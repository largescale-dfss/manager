import manager_django_pb2
import random
from grpc.beta import implementations
import grpc
import time
import os

_ONE_DAY_IN_SECONDS = 24 * 60 *60

class Manager(manager_django_pb2.BetaManagerServicer):
  def SaveFile(self, request, context):
    finalMessage = "Inside SaveFile()!"

    #SaveFile request has file, filepath, and timestamp
    saveFile = request.save_file
    path = request.save_path
    timestamp = request.timestamp

    filename = os.path.basename(path)

    with open(filename, 'wb') as f:
        f.write(saveFile)

    return manager_django_pb2.SaveResponse(transfer_status='%s' % finalMessage)


#Host Manager Server
def serve():
    #Reading off of the manager.proto, creating Manager class
    server = manager_django_pb2.beta_create_Manager_server(Manager())
    server.add_insecure_port('[::]:50050')
    server.start()
    try:
      while True:
          time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
  serve()



'''
  def Elaborate(self, request, context):
    topic = request.topic
    run = request.blah_run

    if run == []:
        finalMessage = topic + " "
        finalMessage = finalMessage[:-1]
        return debate_pb2.ElaborateReply(answer='%s' % finalMessage)

    if len(run) == 1:
        finalMessage = "blah" * run[0] + " " + topic
    else:
        finalMessage = "blah" * run[0]
        for blah in run[1:]:
            finalMessage += " " + topic + " blah" * blah

    return debate_pb2.ElaborateReply(answer='%s' % finalMessage)
'''