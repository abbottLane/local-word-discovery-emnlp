import hfst
import re

def main():
    hfst = HFSTModel('evaluation/transducers/kunwok-acceptor.min.bin.hfst')
    hfst.test_cmd_line()

class HFSTModel:
    def __init__(self, modelPath):
        super().__init__()
        self.modelPath = modelPath
        self.hfst_process = hfst.HfstInputStream(self.modelPath)
        self.fst = self.hfst_process.read()

    def test_cmd_line(self):
        results = self._clean_ranked_hfst_results(list(self.fst.lookup("hfdkljslksdkldskabirribengkandfshksds"))) # lookup word
        print(results)

    def _clean_ranked_hfst_results(self, results):
        results = [(re.sub("\@.*?\@", "", x[0]), x[1]) for x in list(results)] # strip out flag diacritics
        # remove duplicates while preserving ranked order
        seen = {}
        deduped_results = []
        for r in results:
            if r[0] not in seen:
                deduped_results.append(r[0]) #  + "::" + str(r[1]) <-- for debugging weights
                seen[r[0]] = r[1]
        # return clean results
        return deduped_results

    def apply_down(self, word):
        return self._clean_ranked_hfst_results(list(self.fst.lookup(word))) # lookup word




if __name__=="__main__":
    main()
