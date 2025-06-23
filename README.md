These are the version you cannot see:<br>
Version 0: adding trackie_scrapepr<br>
Version 1: adding sssad_scrapper<br>
Version 2: added noramalize_functions<br>
Version 3: added sssad_data_scrapper (Track Part)<br>
Version 4: added sssad_data_scrapper (Field Part)<br>
Version 5: added example_usage_for_code<br>
Version 6: Fix bugs in trackie scrapper<br>
Version 7: added run_scrappers<br>
Version 8: build out the layout for the html website<br>
Version 9: Added styles<br>
version 10: Added logic for showing the data -> choose_meet<br>
version 11: Added logic for showing data -> school<br>
Version 12: Generalize filter by school logic to fit Gender, Event Type, Event, Category, Choose Time and Event<br>
version 13: Added Search filter<br>
version 14: Fix some minor bugs<br>
version 15: Added live search and more comments<br>
___

**There are ALOTS alot alot of malformed data in trackie website and sssad website so my scrapping won't be 100% correct**
<br>
**Some time there are categories like Unknown which is basically impossible to parse**
<br>
**Cannot parse championships game due to ambiguity and different format**
<br>
**To use this code**
<br>
<br>
First install these pakages
pip if you do not already had it<br>
after use these commandas <br>
pip install webdriver-manager <br>
pip install selenium <br>
pip install pandas <br>
pip install Flask <br><br>
then after that to run the code just go to the main file then run it 
after you run the code you should see something like this
<br><br>
 * Serving Flask app 'main' <br>
 * Debug mode: on <br>
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead. <br>
 * Running on http://127.0.0.1:5000 <br>
Press CTRL+C to quit <br>
 * Restarting with stat <br>
 * Debugger is active! <br>
 * Debugger PIN: 466-346-204 <br>
127.0.0.1 - - [22/Jun/2025 21:26:26] "GET / HTTP/1.1" 200 - <br>
127.0.0.1 - - [22/Jun/2025 21:26:26] "GET /static/style.css HTTP/1.1" 200 - <br>
127.0.0.1 - - [22/Jun/2025 21:26:26] "GET /static/main.js HTTP/1.1" 200 - <br>
127.0.0.1 - - [22/Jun/2025 21:26:26] "GET /static/main.js HTTP/1.1" 200 - <br>
loading initial data <br>
127.0.0.1 - - [22/Jun/2025 21:26:26] "POST /load_initial_data HTTP/1.1" 200 - <br>
<br>
ctrl+click on the link displayed
___

PROJECT BY MINH (ANDREW) HUY NGUYEN

<br>
github_link
<br>
https://github.com/fntionalProgramming/Track-Meet-Manager-2
