class LabelPrinter:
    def __get_pdf_path(self) -> str:
        pdf_name = self.__pdf_name_template.format(
            data=self.__data,
            title_hash=hashlib.sha1(self.__title.encode()).hexdigest())
        return os.path.join(self.__print_cache_dir, pdf_name)

