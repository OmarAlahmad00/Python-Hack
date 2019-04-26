# Python-Hack
There are two files in this project. There is the "Connector" and there is the "Client". 
The Connector is the Host who will be controlling the Client, the victim.
I used the "pynput" module to help me with the keystrokes.
The reason that there are two shutdown commands on the client because people found out that
the program is located at the startup folder so I had to disable the run (WIN + R) window
since that was how they went to the startup folder (shell:startup)
The next way that they disabled the program was through task manager.
Which mean that I had to try and end it. For this I used a shell command.
If task manager was open it would return a certain number and then shutdown.
If not, it will do nothing.
If you any suggestions for this program, please add it.

******THERE IS A BUG******
The 'r' keystroke does not get sent to the mySQL database. It is an easy fix but I am too lazy to do it. Not really important. :D
