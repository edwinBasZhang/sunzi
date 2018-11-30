from flask import Flask,render_template
import sys
app = Flask(__name__)


@app.route('/')
def hello_world():
    itemcf=[]
    item_cf={}
    file = open("/Users/lvqianqian/Downloads/machine learning/Recommendation system/bishe/result_itemcf.txt")
    for line in file.readlines():
        s=line.split(",")
        s[0]=s[0].replace("\""," ")
        s[0] = s[0] + ")"
        s[1]=s[1].replace("\n"," ")
        s[1] = "(" + s[1]
        item_cf={"name":s[0],"grade":s[1]}
        itemcf.append(item_cf)
    length=len(itemcf)
    file.close()

    usercf=[]
    user_cf={}
    file = open("/Users/lvqianqian/Downloads/machine learning/Recommendation system/bishe/result_usercf.txt")
    for line in file.readlines():
        print(line)
        s=line.split(",")
        s[0] = s[0].replace("\"", " ")
        s[0] = s[0] + ")"
        s[1] = s[1].replace("\n", " ")
        s[1] = "(" + s[1]
        user_cf = {"name": s[0], "grade": s[1]}
        usercf.append(user_cf)
    print(usercf)
    length_user=len(usercf)
    file.close()

    apriori=[]
    apriori_i={}
    file = open("/Users/lvqianqian/Downloads/machine learning/Recommendation system/bishe/last_result_ap.txt")
    for line in file.readlines():
        print(line)
        apriori_i = {"name": line}
        apriori.append(apriori_i)
    length_apr=len(apriori)
    file.close()

    fpgrowth=[]
    fpgrowth_i={}
    file = open("/Users/lvqianqian/Downloads/machine learning/Recommendation system/bishe/last_result_fp.txt")
    for line in file.readlines():
        print(line)
        fpgrowth_i = {"name": line}
        fpgrowth.append(fpgrowth_i)
    length_fp=len(fpgrowth)
    file.close()

    return render_template('test.html',itemcf=itemcf,length=length+1,usercf=usercf,
                           length_user=length_user+1,apriori=apriori,length_apr=length_apr+1,
                           fpgrowth=fpgrowth,length_fp=length_fp+1
                           )


if __name__ == '__main__':
    app.run()
