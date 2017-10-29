class LabelPrinter:
    def __generate_pdf(self):
        pdf_generator = _LabelPdfGenerator()
        pdf_generator.generate_label(
            self.__title, self.__data, self.__logo_path, config.App.LABEL_BORDER,
            output_path=self.__pdf_path)


    def __prepare_print_cache_dir(self):
        os.makedirs(self.__print_cache_dir, exist_ok=True)



    def __get_pdf_path(self) -> str:
        pdf_name = self.__pdf_name_template.format(
            data=self.__data,
            title_hash=hashlib.sha1(self.__title.encode()).hexdigest())
        return os.path.join(self.__print_cache_dir, pdf_name)
