
class LabelPrinter:
    def print(self, printer: (Printer, None)=None, copies: int=1):
        printer = printer or Printer(config.App.LABEL_PRINTER)

        self.print_to_pdf()
        printer.print_pdf(self.__pdf_path, options={'copies': str(copies)})
