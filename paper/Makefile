xe:
	-xelatex -interaction=nonstopmode main.tex
	-bibtex  main.aux
	-xelatex -interaction=nonstopmode main.tex
	-xelatex -interaction=nonstopmode main.tex
pdf:
	-pdflatex -interaction=nonstopmode main.tex
	-bibtex  main.aux
	-pdflatex -interaction=nonstopmode main.tex
	-pdflatex -interaction=nonstopmode main.tex
main:
	-pdflatex -interaction=nonstopmode main.tex
	-bibtex  main.aux
	-pdflatex -interaction=nonstopmode main.tex
	-pdflatex -interaction=nonstopmode main.tex
clean:
	find . -name '*.aux' -print0 | xargs -0 rm -rf
	rm -rf *.lof *.log *.lot *.out *.toc *.bbl *.blg *.thm
docx:
	pandoc main.tex -o output.docx \
	--resource-path=.:figures \
	--filter pandoc-crossref \
	--reference-doc=my_temp.docx \
	--number-sections \
	-M autoEqnLabels \
	-M tableEqns \
	-M reference-section-title=Reference \
	--bibliography=my_ref.bib \
	--citeproc \
	--csl ieee.csl \
	--extract-media=figures

sstdocx:
	pandoc ./SST/SST_main.tex -o ./SST/SST_output.docx \
	--resource-path=.:figures \
	--filter pandoc-crossref \
	--reference-doc=my_temp.docx \
	--number-sections \
	-M autoEqnLabels \
	-M tableEqns \
	-M reference-section-title=Reference \
	--bibliography=my_ref.bib \
	--citeproc \
	--csl ieee.csl \
	--extract-media=figures