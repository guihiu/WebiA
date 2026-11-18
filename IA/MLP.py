"""
this class create a interface, for MLP and layes


"""

class Dense():
    def __init__(self,N_neuron:int,activation):
        self.N_neuron=N_neuron
        self.activation=activation
        #self.N=N

    
    def __str__(self):
        return (f"{self.N_neuron}, com função de ativação{self.activation}, com parametro N={self.N} ")
        #return (f"{self.N_neuron}, com função de ativação{self.activation}, com parametro N={self.N} ")

class Dropout():
    def __init__(self,N):
        self.N=N
        

class Net():
    def __init__(self, layer_in:Dense,layer_out:Dense, layer_hidden:{Dense}):
        self.layer_in=layer_in
        self.layer_out=layer_out
        self.layer_hidden= layer_hidden
        

    def __str__(self):
       return (f" o numero de epocas e de: {self.epocs} o numero maximo de {self.max_inter} e o metodo de apreendizagem: {self.solver}, ")

class config():
    def __init__(self, epocs,max_inter, solver):
        self.epocs=epocs
        self.max_inter= max_inter
        self.solver=solver



if __name__== '__main__':
    layer_in=Dense(5,"Softmax")
    layer_out=Dense(10,"ReLU")
    l1=Dense(16,"Softmax")
    l2=Dense(16,"Softmax")
    l3=Dense(16,"Softmax")
    layer_hidden={l1,l2,l3}

    ia=Net(layer_in, layer_out, layer_hidden, 1000,0.1,"derivia")
    print(ia)