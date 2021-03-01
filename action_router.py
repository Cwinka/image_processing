from main import ImageGraph
from downsize import SizeReducer

class Router:
    action_list = {
        'dither': "Dither",
        'dither_gray': "Dither gray",
        'to_gray': "Convert to gray",
        'lower_size': "Lessen size",
        'save': "Save image",
    }
    workers = [
        
    ]
    def dispatch(self, action:str):
        """ Dispatch action, commonly inside ImageGraph oject """
        if action not in self.action_list:
            raise TypeError(f'Does not supprot [{action}] method.')

        for worker in self.workers:
            try:
                getattr(worker, action)()
            except AttributeError: # if something does not work, remove it
                continue 

    def add_workers(self, workers):
        for worker in workers:
            self.workers.append(worker)
        

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