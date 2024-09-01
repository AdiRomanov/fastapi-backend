
## Ghid pentru Mediul de Lucru #RO (English below)

### Instalare și Configurare 

Pentru a rula aplicația, este important să folosim `virtualenv` pentru a crea spații izolate de Python. Aceasta este o practică esențială, deoarece vom utiliza multiple librării cu versiuni specifice, și trebuie să evităm conflicte cu alte versiuni care ar putea fi deja instalate pe sistemul vostru.

1. **Instalare Python și Virtualenv**
   - Instalați Python pe sistemul vostru.
   - Instalați Angular.
   - Deschideți terminalul și executați: `pip install virtualenv`

2. **Configurare Virtual Environment**
   - Directorul de baza este ex:`PS C:\Users\Adi\Desktop\ProiectColectiv\NumeProiect>`.
   - După instalarea Python, deschideți terminalul in directorul de baza al proiectului și executați următoarele comenzi pentru a va crea propriul `virtual env`
   - Directorul `venv` este default un fisier inclus in .gitignore asa ca nu va fi uploadat pe GitHub.
   - (Eu foloses PyCharm Professional, e gratis pentru studenti):
     ```bash
     python -m venv venv (comanda asta se foloseste o singura data, la inceput, dupa o sa aveti fisierul venv creat si va fi nevoie numai de urmatoarele doua comenzi)
     cd .\venv\
     .\Scripts\activate
     ```
   - Pentru a naviga in directorul de baza folositi comanda:
    ```bash
    cd ..
    ```

   Terminalul, in directorul de baza, ar trebui să arate așa cu `(venv)` in fata:
   ```bash
   (venv) PS C:\Users\Adi\Desktop\ProiectColectiv\NumeProiect>
    ```
    Pentru a ieși din mediu virtual, utilizați comanda: `deactivate`. Astfel, veți reveni la directorul de bază: `PS C:\Users\Adi\Desktop\ProiectColectiv\NumeProiect>`

    NOTĂ: Nu ieșiți din mediu virtual dacă nu aveți un motiv specific.

### Instalare Librării și Dependințe

1. **Actualizare Librării**
   - Asigurați-vă că sunteți în directorul de bază, iar terminalul arată astfel:
    ```bash
   (venv) PS C:\Users\Adi\Desktop\ProiectColectiv\NumeProiect>
    ```
   - Pentru a instala librăriile necesare, utilizați comanda: `pip install -r .\requirements.txt`
   - După fiecare instalare sau adăugare a unei noi librării, actualizați requirements.txt cu comanda: `pip freeze > requirements.txt`


    NOTĂ: Rulati aceste comenzi de fiecare data cand:
    
        Intrati sa lucrati la proiect: `pip install -r .\requirements.txt`.
        
        Ati terminat de lucrat: `pip freeze > requirements.txt` 

        !!!!!! NU UITATI SA FITI IN DIRECTORUL DE BAZA: `PS C:\Users\Adi\Desktop\ProiectColectiv\NumeProiect>` 


### Pornire Server Local

1. **FastApi Server**
   - Navigați în directorul components_controller cu comanda `cd`:
    ```bash
    (venv) PS C:\Users\Adi\Desktop\ProiectColectiv\NumeProiect>
    ```
   - Pentru a porni serverul FastApi, utilizați comanda: `uvicorn app.main:app`
   - Accesați http://127.0.0.1:8000/ în browser (folositi mod incognito pentru ca s-ar putea sa aveti probleme cu cache-ul).
   - Pentru oprire, utilizați `CTRL + C` in terminal.
2. **Front-End Development**
   - Terminalul pentru serverul de FastApi trebuie lasat deschis.
   - Deschideți un terminal nou pentru partea de front-end si navigați în directorul frontend cu comanda `cd`:
    ```bash
    (venv) PS C:\Users\Adi\Desktop\ProiectColectiv\NumeProiectFrontend>
    ```
   - Pentru a porni serverul front-end, utilizați comanda: `ng serve`
   - Acest lucru va actualiza automat site-ul la fiecare salvare (CTRL + S).
   - Pentru a opri execuția, utilizați `CTRL + C`.
   

    Cu aceste setări, veți avea un mediu de lucru funcțional pentru proiectul dumneavoastra.




## Guide for Working Environment #EN

To run the application, it is important to use `virtualenv` to create isolated spaces for Python. This is essential because we will use multiple libraries with specific versions, and we need to avoid conflicts with other versions that may already be installed on your system.

1. **Install Python and Virtualenv**
   - Install Python on your system.
   - Install Angular on your system.
   - Open the terminal and run: `pip install virtualenv`

2. **Configure Virtual Environment**
   - The base directory is for example `PS C:\Users\Adi\Desktop\ProiectColectiv\MyProject>`.
   - After installing Python, open the terminal in the base directory and run the following commands to create your own `virtual env`. 
   - The `venv` directory it's by default included in the .gitignore file, its not going to be uploaded on GitHub.
   - (I use Pycharm Professional, it is free for students):
     ```bash
     python -m venv venv (this command is used only once, at the begging, after that you will have the venv folder created and you will need only the following two commands)
     cd .\venv\
     .\Scripts\activate
     ```
   - To navigate to the base directory, use the command:
    ```bash
    cd ..
    ```

   The terminal in the base directory should show `(venv)`:
   ```bash
   (venv) PS C:\Users\Adi\Desktop\ProiectColectiv\MyProject>
    ```
    To exit the virtual environment, use the command: `deactivate`. This will return you to the base directory: `PS C:\Users\Adi\Desktop\ProiectColectiv\MyProject>`

    NOTE: Do not exit the virtual environment unless you have a specific reason.

### Install Libraries and Dependencies

1. **Update Libraries**
   - Ensure you are in the base directory, and the terminal looks like this:
    ```bash
   (venv) PS C:\Users\Adi\Desktop\ProiectColectiv\MyProject>
    ```
   - To install the required libraries, use the command: `pip install -r .\requirements.txt`
   - After each installation or adding a new library, update `requirements.txt` with the command: `pip freeze > requirements.txt`

   NOTE: Run these commands each time you:
    
        Start working on the project: `pip install -r .\requirements.txt`.
        
        Finish working: `pip freeze > requirements.txt` 

        !!!!!! DON'T FORGET TO BE IN THE BASE DIRECTORY: `PS C:\Users\Adi\Desktop\ProiectColectiv\MyProject>` 


### Start Local Server

1. **FastApi Server**
   - Navigate to the components_controller directory with the `cd` command:
    ```bash
    (venv) PS C:\Users\Adi\Desktop\ProiectColectiv\MyProject>
    ```
   - To start the FastApi server, use the command: `uvicorn app.main:app`
   - Access [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in the browser (use incognito mode as you might have cache issues).
   - To stop the execution, use `CTRL + C` in the terminal.
2. **Front-End Development**
   - Keep the terminal for the FastApi server open.
   - Open a new terminal for the front-end part and navigate to the frontend directory with the `cd` command:
    ```bash
    (venv) PS C:\Users\Adi\Desktop\ProiectColectiv\MyFrontEnd
    ```
   - To start the front-end server, use the command: `ng serve`
   - This will automatically update the site on each save (CTRL + S).
   - To stop the execution, use `CTRL + C`.
  

   With these settings, you will have a functional working environment for you'r project.
