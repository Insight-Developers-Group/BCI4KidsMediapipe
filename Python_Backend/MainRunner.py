from asyncio.windows_events import NULL
import socket
import AnswerGenerator
import StateGenerator
import DFGenerator

# Setup the socket properties
# Standard loopback interface address (localhost) - this is the name of the docker network
HOST = socket.gethostbyname('insight_project')
PORT_1 = 9898        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT_1))
    s.listen()
    conn, addr = s.accept()  # accepting the socket from the connection

    # Queue of images to be processed Tuple of <Type, img>
    img_queue = []

    # Two types of Generators
    facialDFGenerator = None  # TODO MAKE THIS THE ACTUAL DATA TYPE
    irisDFGenerator = None  # TODO MAKE THIS THE ACTUAL DATA TYPE

    # Initiate State Generator with the appropriate models
    stateGenerator = None  # TODO MAKE THIS THE ACTUAL DATA TYPE

    # Two types of Generators
    facialAnswerGenerator = None  # TODO MAKE THIS THE ACTUAL DATA TYPE
    irisAnswerGenerator = None  # TODO MAKE THIS THE ACTUAL DATA TYPE

    FACE = "FACE"
    IRIS = "IRIS"

    with conn:
        print('Connected by', addr)

        # Dummy code to echo what is entered by the client
        ############################################# START OF DUMMY CODE #############################################
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            
        ############################################# END OF DUMMY CODE ################################################


            
            # Recieve image from connection and decode as necessary

            # Place it in a queue of images
            # Reference for working with Queues
            # https://www.geeksforgeeks.org/queue-in-python/

            while len(img_queue) > 0:
                img = img_queue.pop()
                # Use the generator based on the imageType
                df = None
                if (img[0] == FACE):
                    # df = facialDFGenerator.generateLandmarks(img[1])
                    pass
                elif (img[0] == IRIS):
                    # df = irisDFGenerator.generateLandmarks(img[1])
                    pass 
                else:
                    # Send an error message through the socket
                    continue

                # Run Machine learning algorithm based on type
                # state = stateGenerator.getState(img[0], img[1])

                # Run the Answer Generator
                answer = None
                if (img[0] == FACE):
                    # answer = facialAnswerGenerator.getAnswer(img[1])

                elif (img[0] == IRIS):
                    # answer = irisAnswerGenerator.getAnswer(img[1])

                    # If the answer is a nonetype it means not enough frames have been processed to give an answer - continue
                if (answer == None):
                    continue

                # Send the response to the frontend
                conn.sendall(answer)
