import sys
import os
import bs4
import urllib2
import urllib
BASE_URL = "http://arxiv.org"
HEP_URL = 'http://arxiv.org/abs/hep-th/%d'

# TODO: Change prints to logs


def get_pdf(paper_id, save_dir):
    file_path = os.path.join(save_dir, str(paper_id) + ".pdf")
    if not os.path.isfile(file_path):
        # Only try to download missing files
        try:
            paper_page = urllib2.urlopen(HEP_URL % paper_id)
            soup = bs4.BeautifulSoup(paper_page.read().decode('utf8'))
        except:
            print "Error"
        else:
            # TODO: Check if this pattern holds for all papers
            file = soup.find("a", {"accesskey" : "f"})
            if file:
                file_url = file["href"]
                print os.path.join(save_dir, str(paper_id) + ".pdf")
                urllib.urlretrieve(BASE_URL + file_url, os.path.join(save_dir, str(paper_id) + ".pdf"))
            else:
                print "Unable to find PDF: %d" % paper_id


def main():
    if len(sys.argv) > 2 and sys.argv[1].isdigit() and os.path.isdir(sys.argv[2]):
        get_pdf(int(sys.argv[1]), sys.argv[2])
    else:
        print "Usage <paper id> <destination directory>"

if __name__ == "__main__": main()
