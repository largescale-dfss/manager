from grpc.beta import implementations

import sys
import manager_django_pb2

_TIMEOUT_SECONDS = 100

def sendFile(file, filePath, timestamp):
  channel = implementations.insecure_channel('localhost', 50051)
  stub = manager_django_pb2.beta_create_Manager_stub(channel)
  if sys.argv[1] == "answer":
    response = stub.Answer(debate_pb2.AnswerRequest(question=sys.argv[2], timeout=int(sys.argv[3])), _TIMEOUT_SECONDS)
  elif sys.argv[1] == "elaborate":
    finalArray = []
    for num in sys.argv[3:]:
        finalArray.append(int(num))
    response = stub.Elaborate(debate_pb2.ElaborateRequest(topic=sys.argv[2], blah_run=finalArray), _TIMEOUT_SECONDS)
  else:
      return 0

  print response.answer


