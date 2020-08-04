##############################################################################
## Merge PDF files based on a LIST of input_paths and an output_path 
## Merging will happen in input order
#############################################################################

def merge_pdf(input_paths, output_path):
    
    from PyPDF2 import PdfFileReader, PdfFileWriter
    
    if type(input_paths) == list:
    
        pdf_writer = PdfFileWriter()

        for path in input_paths:
            pdf_reader = PdfFileReader(path)

            for page in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page))

        with open(output_path, 'wb') as fh:
            pdf_writer.write(fh)
            
    else:
        print("INPUT SHOULD BE A LIST")
