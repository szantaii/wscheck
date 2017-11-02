class LabelPrinter:
   def __generate_pdf(self):
        pdf_generator = _LabelPdfGenerator()
        pdf_generator.generate_label(
            self.__title, self.__data, self.__logo_path, config.App.LABEL_BORDER,
            output_path=self.__pdf_path)
