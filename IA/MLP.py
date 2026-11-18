"""
this class create a interface, for MLP and layes


"""

class layer():
    def __init__(self,N_neuron:int,activation, N:float):
        self.N_neuron=N_neuron
        self.activation=activation
        self.N=N

    def __str__(self):
        return (f"{self.N_neuron}, com função de ativação{self.activation}, com parametro N={self.N} ")


class IA():
    def __init__(self, layer_in:layer,layer_out:layer, layer_hidden:{layer}, epocs,max_inter, solver):
        self.layer_in=layer_in
        self.layer_out=layer_out
        self.layer_hidden= layer_hidden
        self.epocs=epocs
        self.max_inter= max_inter
        self.solver=solver

    def __str__(self):
       return (f" o numero de epocas e de: {self.epocs} o numero maximo de {self.max_inter} e o metodo de apreendizagem: {self.solver}, ")
       """ print("A camada de entrada tem:"+self.layer_in)
        for i in layer_hidden:
            print("A camada oculta {i}:"+ self.layer_hidden[i])
        print("A camada de saida tem:"+self.layer_out)"""



if __name__== '__main__':
    layer_in=layer(5,"Softmax",0.1)
    layer_out=layer(10,"ReLU",0.1)
    l1=layer(16,"Softmax",0.1)
    l2=layer(16,"Softmax",0.1)
    l3=layer(16,"Softmax",0.1)
    layer_hidden={l1,l2,l3}

    ia=IA(layer_in, layer_out, layer_hidden, 1000,0.1,"derivia")
    print(ia)