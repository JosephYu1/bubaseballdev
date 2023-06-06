# Capstone
Baylor 2023 Spring DSC43C9

---

## Goal of the Project

To create an interactive environment for the Baylor Baseball team to explore and analyze the TrackMan™ data generated.  
The aim is a relatively simple graphical interface for the user to interact with the data without extensive knowledge in statistics or data science.  

---

## Libraries and Setup

See requirements.txt
We mainly use Dash for easier development due to time constraints.

---

## Running the app in Python

Run main.py

---

## Program Structure

The program is kept intentionally flat for easier collaboration.  
The key files are:  

- main.py
- ids.py
- layout.py
- callback.py

The main uses layout to set visual components positions, and the callback listens to actions done on the graphical interface.
This program is designed to both run as a standalone program and also be hosted on servers to run remotely.

---

## About Memory Usage and Performance  

The program is not going to run fast, mainly due to 3 reasons:  

1. Storage into memory and data conversion
2. Large data calculations using Python/Pandas
3. Plotting takes time  

The idea for 1 is to cut down on data usage, since the Baseball team may travel to a different state and may have subpar  
internet connection. Not to mention the data itself is not small - at least 30 MB and will only grow larger overtime. Because  
of this, we decided to cache some of the data in the browser. However, due to Dash's limitation, we can only store things in a  
JSON serializable format, but our calculations uses Pandas Dataframe... this means each time some filtering needs to be  
done/undone, we'd need to convert a JSON dictionary back into dataframe before we can operate on it. As you can imagine, this  
is expensive to do repeatedly. However, it's a trade off that makes sense.  
For 2, it's possible to speed up the program by running Pyspark instead, or rewrite in another faster language. However, converting  
between a Pyspark dataframe and a JSON dictionary would take a even longer time, so the trade-off may or may not justify it, depending  
the implementation.  
For 3, since we are using Plotly Express to plot graphs, this is as fast as plotting can go without writing our own library.  

---

## Members contact:

### Advisor

Dr. Greg Speegle: Greg_Speegle@baylor.edu

### Students

- Daniela Cortes Bermudez: Daniela_CortesBermu1@baylor.edu
- Ivan Ko: ivan_ko1@baylor.edu
- Ayo Omolewa: ayomide_omolewa1@baylor.edu
- Claire Teng: claire_teng1@baylor.edu
- Ty Wicks: ty_wicks1@baylor.edu
