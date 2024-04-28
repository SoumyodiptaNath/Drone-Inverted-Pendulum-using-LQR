from SOURCE import train, test

#MAIN FUNCTION
if __name__ == "__main__":
    if int(input("Enter: \n1 to train \n0 to test\n->")):
        app = train.App()
    else:
        app = test.App()
    app.mainloop()
