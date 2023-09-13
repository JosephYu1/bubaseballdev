# bubaseballdev
  This is the repository for the development and maintaince of the BU baseball Web App on the development server.  

#### Prerequisites: ####
##### Python Environment #####
  The application requires python packages from the file [`env_setup/server_config.yml`](https://github.com/JosephYu1/bubaseballdev/blob/main/env_setup/server_config.yml)

##### Example Environment Setup with Conda #####
  With Anaconda installed and avaiable on your machine, with the python package requirements file [`env_setup/server_config.yml`](https://github.com/JosephYu1/bubaseballdev/blob/main/env_setup/server_config.yml)

  ```bash
  conda env create -f /path/of/file/server_config.yml
  conda activate server_config
  ```

---

#### Installation Guide: ####

##### Start in Debug Mode #####
  1. Clone the git repo onto your local machine or server.
  2. Download and place all data files within the specified data directories, follow this [link_under_construction](https://github.com/JosephYu1/bubaseballdev/blob/capstone23_liftover/) for detailed instructions.
  3. Within the top level within the cloned repo directory, run `python main.py` on your console.
  4. You have succesfully started your application if the console output shows:
        
         Dash is running on http://127.0.0.0.1:8050/

          * Serving Flask app 'app'
          * Debug mode: on
         
##### Example Quick Start in Server Mode with uWSGI #####
  1. Clone the git repo onto your local machine or server.
  2. Download and place all data files within the specified data directories, follow this [link_under_construction](https://github.com/JosephYu1/bubaseballdev/blob/capstone23_liftover/) for detailed instructions.
  3. Confirm that the [`wsgi.py`](https://github.com/JosephYu1/bubaseballdev/blob/main/wsgi.py) is present in the top level directory within the cloned repo.
  4. Confirm that your local machine or server allows traffic on port to be used for serving the web application (port **80** in our example).
  5. Within the top level within the cloned repo directory, run 
     ```bash 
     sudo /file/path/to/executable/for/uwsgi --socket 0.0.0.0:80 --protocol=http -w wsgi
     ```
  5. In a web browser, enter the ip address/domain name for the local machine or server, and the application may be visible in the web browser.
 
---

#### Baylor Developers Only: ####
##### SSH Tunneling with BU Servers #####
To tunnel with Baylor University servers so that your local machine can listen to remote server ports, perform the following steps:
    1. Open a terminal on your local machine.
    2. input the follow command
        ```bash
        ssh -L <port number on local machine>:localhost:<port number on remote server> <remote server address>
        ```
    3. Then any application that is served on the port number on the remote server should now be accessible on the local machine on the specified port number.
    4. Go to a browser on a local machine and go to the address localhost:port_number_of_local_machine


---
#### Authors ####

  Greg Speegle, Ph.D., Departmenat of Computer Science, Baylor Univesity    
  Yutai Xue, Department of Computer Science, Baylor University
  Joseph Yu, Department of Computer Science, Baylor University


##### Acknowledgements #####

Baylor Data Science Capstone 23 Team members

