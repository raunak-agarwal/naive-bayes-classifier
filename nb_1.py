import pandas as pd

class Classifier():
    data = None
    class_attr = None
    prior = {}
    cp = {}
    hypothesis = None
    sizes = {}
    k = 0

    def __init__(self,filename = None, class_attr = None, k = 1.0):
        self.data = pd.read_csv(filename, sep=',', header =(0))
        self.class_attr = class_attr
        self.k = float(k)


    def calculate_prior(self):          # calculate probabilities for the class_attribute i.e. 'Play'
        class_values = list(set(self.data[self.class_attr]))
        class_data =  list(self.data[self.class_attr])
        for i in class_values:
            self.prior[i]  = class_data.count(i)/float(len(class_data))
        print (self.prior)

    def set_sizes(self):
        names = list(self.data)
        self.sizes = {}
        for i in names:
            self.sizes.update({i : len(set(self.data[i]))})
        print(self.sizes)

    def get_cp(self, attr, attr_type, class_value):
        data_attr = list(self.data[attr])
        class_data = list(self.data[self.class_attr])
        total = int(self.k)
        for i in range(0, len(data_attr)):
            if (class_data[i] == class_value and data_attr[i] == attr_type):
                total+=1
        calculation = total/float(class_data.count(class_value) + self.k*self.sizes[attr])

        print("P (", attr, "=", attr_type, "| Play = ", class_value, ") = (", str(total), "+", self.k, ") / (" , self.sizes[attr], "+",
            str(self.k), "*", str(float(class_data.count(class_value))),") = ",(calculation))
        return calculation

    '''
        Here we calculate Likelihood of Evidence and multiple all individual probabilities with prior
        (Outcome|Multiple Evidence) = P(Evidence1|Outcome) x P(Evidence2|outcome) x ... x P(EvidenceN|outcome) x P(Outcome)
        scaled by P(Multiple Evidence)
    '''
    def calculate_conditional_probabilities(self, hypothesis):
        for i in self.prior:
            self.cp[i] = {}
            for j in hypothesis:
                self.cp[i].update({ hypothesis[j]: self.get_cp(j, hypothesis[j], i)})
 

    def classify(self):
        print ("\nResult with Laplacian smoothing:")
        h = []
        for i in self.cp:                   
            agg = 1
            f = self.cp[i].values()        # can also be reduced by a simple lambda reduce(lambda x, y: x*y, self.cp[i].values())*self.prior[i]
            for j in f:
                agg = agg*j                     
            g = self.prior[i]
            h.append(g*agg)
            print (i, " --> ", g*agg)
            

if __name__ == "__main__":
    print("\n\tWelcome to the naive bayes classifying program for tennis.csv\n")
    k_lap = input("Please enter the value of 'k' for Laplacian smoothing: ")
    c = Classifier(filename = "tennis.csv", class_attr = "Play", k = k_lap)
    print("The prior probabilities for 'yes' and 'no' in the 'Play' column are:")
    c.calculate_prior()
    print("\nThe sizes of the rest of the attribute columns are: ")
    c.set_sizes()

    outlook = input("\nProvide conditions for Outlook (sunny/overcast/rainy): ")
    temp = input("Provide conditions for temperature (hot/mild/cool): ")
    humidity = input("Provide conditions for humidity (high/normal): ")
    windy = input("Is it windy? (true/false): ")
    c.hypothesis = {"Outlook":outlook, "Temp.":temp, "Humidity":humidity , "Windy":windy}

    print("\nThe conditional probabilities are as follows:")
    c.calculate_conditional_probabilities(c.hypothesis)
    c.classify()
