import os
import re
from pypdf import PdfReader, PdfWriter, PdfMerger

root_folder = os.getcwd()
os.chdir( root_folder )


fcra_base = re.compile(r'(?i)^FCRA\w*\.pdf$')
fcra_audit = re.compile(r'(?i)^Audit\w*\.pdf$')

print("\nHow do you want to modify the files?\n")

print("1) Remove page one from FCRA.\n")
print("2) Combine FCRA and Audit.\n")
print("3) Combine both and remove page 1.\n\n")
print("Please make sure the files are named FCRA and Audit")

response = input("Please enter one of the (numbers) above\n")

def remove_FCRA_page_one():
    for file_name in files:
        # check if the file is named FCRA
        if fcra_base.match(file_name):
            # open the PDF in read mode
            with open(os.path.join(root_folder, file_name), 'rb') as file:
                # read PDF with pydf2
                pdf = PdfReader(file)
                # create a PdfWriter object to write the extracted PDFs
                writer = PdfWriter()

                for page_num in range(1, len(pdf.pages)):
                    writer.add_page(pdf.pages[page_num])
                # write the page selection to disk
                with open(os.path.join(root_folder, f'FCRA.pdf'), 'wb') as output:
                    writer.write(output)
                # print what we did
                parent_folder = os.path.basename(os.path.normpath(root_folder))
                print(f"Removed page 1 from FCRA in {parent_folder}.")

if response == "1":
    for subdir, dirs, files in os.walk(root_folder):
        remove_FCRA_page_one()


target_names = ['fcra', 'audit']

if response == "2" or "3":
    for subdir, dirs, files in os.walk(root_folder):
        audit_file_path = None  # initialize audit_file_path before the loop
        if any(file.lower().startswith(name) for name in target_names for file in files):
            merger = PdfMerger()

            for file in files:
            # check if file matches one of the target_names and is not Audit.pdf
                if file.lower().startswith('audit') and file.endswith('.pdf'):
                    audit_file_path = os.path.join(subdir, file)
                elif any(file.lower().startswith(name) for name in target_names) and file.endswith('.pdf'):
                    file_path = os.path.join(subdir, file)
                    # add file to merger
                    merger.append(file_path)
                    print(f"File '{file}' added to merger in folder '{subdir}'")
            
            if audit_file_path:  # if Audit.pdf exists, add it to the end
                merger.append(audit_file_path)
                print(f"File 'Audit.pdf' added to merger in folder '{subdir}'")

            # output file path for our new PDF within each folder
            fcra_path = os.path.join(root_folder, 'FCRA.pdf')
            audit_path = os.path.join(root_folder, 'Audit.pdf')
            output_path = os.path.join(subdir, 'FCRA2.pdf')

            with open(output_path, 'wb') as output_file:
                merger.write(output_file)
            
            merger.close()

            os.remove(fcra_path)
            os.remove(audit_path)
            os.rename('FCRA2.pdf', 'FCRA.pdf')

            if response == "3":
                remove_FCRA_page_one()