from imageGraph import ImageGraph
from sizeReducer import SizeReducer

class Router:
    workers = [] # list of all instances
    public_f = [
        'quit'
    ] # list of all instances methods.Requeires public_f attribute inside each worker
    def dispatch(self, action:str):
        """ Dispatch action, commonly inside ImageGraph oject """
        if action not in self.public_f:
            print(f'Does not supprot [{action}] method.')
            return
        
        if action == 'quit':
            exit()

        for worker in self.workers:
            # don't want to make try except block
            # to prevent catch some errors inside worker.action func
            if action in dir(worker):
                getattr(worker, action)()
            else:
                continue
    
    def __update_public(self, worker: callable):
        try:
            self.public_f.extend(action for action in worker.public_f)
        except AttributeError:
            raise AttributeError(f"{worker.__class__} has no [public_f] attribute")

    def add_workers(self, workers):
        for worker in workers:
            self.workers.append(worker)
            self.__update_public(worker)
        

if __name__ == "__main__":
    image_url = input("Enter image url or drag image here: ")
    r = Router()
    factor = int(input("Enter factor value (integer): "))

    r.add_workers([
        SizeReducer(image_url),
        ImageGraph.from_image_url(image_url, factor),
    ])

    action = input("Enter action name: ")
    while True:
        r.dispatch(action)
        action = input("Enter action name: ")