class LabelPrinter:
    def __prepare_print_cache_dir(self):
		os.makedirs(self.__print_cache_dir, exist_ok=True)
