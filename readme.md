OpenKorPos
==========

OpenKorPos is a Korean part-of-speech tagging corpus. It is a free, open alternative to the [Sejong corpus](https://www.korean.go.kr/front/reportData/reportDataView.do?mn_id=45&report_seq=197&pageIndex=1) and [Modu corpus](https://corpus.korean.go.kr).

For background of this work, please refer to [our paper](openkorpos.pdf).

Building
--------

Building the corpus requires Python 3.9+, Click, and [Ninja](https://ninja-build.org). You can install all dependencies using the provided `requirements.txt`.

    pip install -r requirements.txt

To build the corpus, you will need to generate the corresponding ninja files, then build.

    python openkorpos.py ningen base
    ninja

You can also enable all the quarantined (flagged) sentences to be included into the generated corpus.

    python openkorpos.py ningen --flagged base

Citing
------

If you need to cite this work before it is made available in the [ACL Anthology bibtex](https://aclanthology.org/anthology.bib.gz), please use the following:

```bibtex
@inproceedings{Moon:LREC2022,
    title = "OpenKorPOS: Democratizing Korean Tokenization with Voting-Based Open Corpus Annotation",
    author = "Moon, Sangwhan and 
              Cho, Won Ik  and 
              Han, Hye Joo  and 
              Okazaki, Naoaki and 
              Kim, Nam Soo",
    booktitle = "Proceedings of the 13th Language Resources and Evaluation Conference (LREC)",
    month = June,
    year = "2022",
    address = "Marseille",
    publisher = "European Language Resources Association",
}
```