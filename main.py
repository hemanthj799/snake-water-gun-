"""
 1 for snake 
 -1 for water 
 0 for gun


"""

compter=-1
youstr=input("Enter your choice: ")
youdict={"snake":1,"water":-1,"gun":0}
you=youdict[youstr]
reversedict={1:"snake",-1:"water",0:"gun"} 

you=youdict[youstr]

print(f"you choose {reversedict[you]}\n computer choose {reversedict[compter]}")

if you==compter:
    print("Game is tie")
elif (you==1 and compter==-1) or (you==-1 and compter==0) or (you==0 and compter==1):
    print("You win")    
elif (you==-1 and compter==1) or (you==0 and compter==-1) or (you==1 and compter==0):
    print("Computer win")  
elif you not in youdict:
        print("Invalid input")

        

