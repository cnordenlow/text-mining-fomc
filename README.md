## Text Mining FOMC

What did Fed say? With the help of text mining, this project aims to gain insights and colour from FOMC Minutes and to make plots out of words.

### Description

### Page

### Technologies



### Methodology


The approach of this project are as follows.

* Words and topics are divided into bag of words of its meaning (e.g. the word "strong" may consists of ["strong", "stronger", "strongest", "strengthen"]).

* Text are divided into sentences aswell as words. For some parts we use the full sentences, and for some we used cleaned sentences and words.

* All sentences are iterated where it checks for the different bag of words and then counted, (e.g. if the word "stronger" is found in a sentence, the count adds one regardless of how many time strong is in the sentence.) For most topics, a second loop followed which counts negative and positive words in the same sentence to get the net sentiment for each topic. 


*The purpose with the bag of words format is to being able to get part  of sentences grouped for their meaning. E.g. for being able to find more colour on asset purchases (tapering amounts, reducing the program, increasing the program), it´s not sufficient to map a sentence with the word of "reduce" and "asset purchase" in the same, but it´s needed to get more of the context for being (more) sure of the meaning.*

The methodology used in this project include use of Python for web parsing and text mining, producing .csv files. R is then used for some additional calculations and to render a Markdown report with vizualisations. Some notes below of the different parts.

</p>



<p>**Web parsing**<br>
All web parsing is done using BeautifulSoup package. The code first parse all .htm pages with the url of "Minutes" in it for the year of interest. Then, a second loop parse all the (chosen) Minutes for the text mining. In both parsing steps, there are a time delay of a couple of seconds.</p>

<p>**Text mining**<br>
With the help of the great package of NLTK, the Minutes are cleaned and converted to a more gentle format. A pretty long(:/) loop are then iterated that runs a set of inner loops for getting the information for each Minutes.</p>

<p>**Vizualisation**<br>
R is used for some further calculations and Markdown for creating a report.</p>



