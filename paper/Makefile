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
