from html.parser import HTMLParser

class ULParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
        self.ul_list = []
        self.depth_list = []
        self.li_content = ''
        self.in_li = False
        self.li_has_content = False
        self.is_ul = False

    def handle_starttag(self, tag, attrs):
        if tag == 'ul':
            self.is_ul = True
            if self.in_li and self.li_content.strip():
                self.ul_list[-1].append(self.li_content.strip())
                self.li_content = ''
                self.li_has_content = True
            self.ul_list.append([])
        elif tag == 'li':
            self.is_ul = False
            self.in_li = True and self.depth_list[-1]
            self.li_content = ''
            self.li_has_content = False
        else: 
            self.is_ul = False
        self.depth_list.append(self.is_ul)

    def handle_endtag(self, tag):
        if tag == 'li':
            if self.in_li and self.depth_list[-2]:
                if self.li_content.strip():
                    self.ul_list[-1].append(self.li_content.strip())
                    self.li_has_content = True
                if not self.li_has_content:
                    self.ul_list[-1].append("")
                self.li_content = ''
                self.in_li = False
        elif tag == 'ul':
            if self.ul_list:
                finished_ul = self.ul_list.pop()
                if self.ul_list:
                    self.ul_list[-1].append(finished_ul)
                else:
                    self.result.append(finished_ul)
        self.depth_list.pop()

    def handle_data(self, data):
        if self.in_li:
            self.li_content += data.strip()
            self.li_has_content = True
