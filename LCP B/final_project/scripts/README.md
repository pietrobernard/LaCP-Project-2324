## CloudVeneto Access
If you use Windows, run Ubuntu from WSL.

### SSH Access
This is to access the remote server via terminal, in text mode. Download the script `tunnel.sh` and run it:
```bash
./tunnel.sh your_cloudveneto_username ssh 2222
```
You will be prompted for your cloudveneto password and for the `g2402` server user password. After you input that, open another terminal and connect to the server via:
```
ssh -p 2222 g2402@localhost
```
you'll be again prompted to enter `g2402`'s password. At this point, you're connected to the server.

### Remote Virtual Desktop
This is to access the remote server with a graphical interface.

#### Start the remote desktop
Download the `vnc.sh` script and run it to start your remote desktop:
```bash
./vnc.sh your_cloudveneto_username -start display_resolution display_number
```
<b>Important</b>:
1. `display_resolution` must be in the format AxB, for instance 1280x1024
2. `display_number` must be $\geq 2$. For instance Tomas had $2$, Mariam $3$ and Andrea had $4$.
When you hit enter, you'll be prompted for your passwords and your remote desktop will start.

#### Open a tunnel to the remote desktop
Download the `tunnel.sh` script and run it:
```bash
./tunnel.sh your_cloudveneto_username vnc port
```
where `port` has to be $\geq 5902$. If your `display_number` was $X$ then you have to choose port $590X$.

After the tunnel is created, you can connect to the virtual desktop via vnc viewer. Open `vnc viewer` and connect to `localhost:port`, so for instance `localhost:5902`.

### Remote Jupyter
You can also run a jupyter server on your virtual desktop and connect to it from your local computer. As before run the `tunnel.sh` script in this manner:
```bash
./tunnel your_cloudveneto_username jupyter 8888
```
As before you'll be prompted the cloudveneto password and the `g2402` username password. When you login, you'll have a tunnel and an ssh connection to the server. At this point, through the terminal, navigate to the folder where you want to launch the jupyter server as you would do in your local computer. At that point, just launch it:
```
jupyter notebook
```
Look at the output on the terminal, you'll see something like:
```
To access the notebook, open this file in a browser:
    file:///home/g2402/.local/share/jupyter/runtime/nbserver-32893-open.html
Or copy and paste one of these URLs:
    http://localhost:8888/?token=5d4c0ef982716a14b831d3eb8c696638a6099c628f3f2b21
or http://127.0.0.1:8888/?token=5d4c0ef982716a14b831d3eb8c696638a6099c628f3f2b21
```
Copy the line starting with `http://localhost:8888` (in the example: `http://localhost:8888/?token=5d4c0ef982716a14b831d3eb8c696638a6099c628f3f2b21`) and <b>paste it in your computer's browser</b>. It will connect, through the tunnel, to the remote server's jupyter notebook.


