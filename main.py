
from flask import Flask, render_template, request, redirect, session, url_for
import psycopg2
from werkzeug.utils import secure_filename

from mylib import make_connection
from mylib import check_photo
import time
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER']='./static/photos'
app.secret_key = "super secret key"

# ----------------------------------Main Index -------------------------------------------------------------------
@app.route('/')
def index():
    cur = make_connection()
    med_id = 17
    sql = "SELECT * FROM medicine WHERE med_id = %s"
    cur.execute(sql, (med_id,))
    n=cur.rowcount
    if n==1:
        data = cur.fetchall()

        return render_template("index.html",item=data)
    else:
        return render_template("index.html", msg="Medicine Not Found")

@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/contact')
def contact():
    return render_template("contact.html")

# -------------------------------------Login----------------------------------------------------------------------
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':

        cur = make_connection()

        a = request.form['T1']
        b = request.form['T2']

        sql = "select * from login where Email='"+a+"' and Password='"+b+"'"
        cur.execute(sql)
        n = cur.rowcount
        if n == 1:
            data=cur.fetchone()
            ut = data[2]
            email = data[0]
            # creating session
            session['email'] = email
            session['ut'] = ut
            if ut=="admin":
                return redirect("admin_home")
            elif ut=="medical":
                return redirect("medical_home")
            else:
                msg = "Error!! User not Found"
        else:
            msg="Error!! Credentials not Found"

        return render_template('Login.html',msg=msg)
    else:
        return render_template("Login.html")

#-------------------------------------logout----------------------------------------------------------------------
@app.route("/logout")
def logout():
    if 'email' in session:
        session.pop('email')
        session.pop('ut')
        return redirect("/login")
    else:
        return redirect("/login")

#--------------------------------------autherror------------------------------------------------------------------
@app.route('/autherror')
def autherror():
    return render_template('AuthError.html')


#------------------------------------Admin Home ------------------------------------------------------------------
@app.route('/admin_home')
def admin_home():
    if 'email' in session:
        ut=session['ut']
        em=session['email']
        if ut=="admin":
            photo = check_photo(em)
            print(photo)
            cur = make_connection()
            sql="select * from admin where Email='"+em+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n == 1:
                data = cur.fetchone()
                return render_template("AdminHome.html",data=data,photo=photo)
            else:
                return render_template("AdminHome.html",msg="No Data Found")
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("login"))

@app.route('/change_admin_photo')
def change_admin_photo():
    if 'email' in session:
        ut=session['ut']
        em=session['email']
        if ut=='admin':
            photo = check_photo(em)
            cur = make_connection()
            sql = "delete from photos where email='"+em+"'"
            cur.execute(sql)
            n=cur.rowcount
            print(n)
            if n==1:
                os.remove("./static/photos/"+photo)
                return render_template("change_admin_photo.html",msg="Success")
            else:
                return render_template("change_admin_photo.html",msg="failure")
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))

@app.route('/admin_photo')
def adminphoto():
    return render_template('photoupload_admin.html')

@app.route('/admin_photo1',methods=['GET','POST'])
def adminphoto1():
    if 'email' in session:
        ut=session['ut']
        em=session['email']
        if ut=="admin":
            if request.method == 'POST':
                file = request.files['F1']
                if file:
                    path = os.path.basename(file.filename)
                    file_ext = os.path.splitext(path)[1][1:]
                    filename = str(int(time.time()))+'.'+file_ext
                    filename = secure_filename(filename)
                    cur = make_connection()
                    sql = "insert into photos values('"+em+"','"+filename+"')"
                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if n == 1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template('photoupload_admin1.html',result="success")
                        else:
                            return render_template('photoupload_admin1.html',result="Failure")
                    except:
                        return  render_template('photoupload_admin1.html',result="Duplicate")
                else:
                    return render_template('photoupload_admin.html')
            else:
                return redirect(url_for("autherror"))
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


#-------------------------------------Medical Home----------------------------------------------------------------
@app.route('/medical_home')
def medical_home():
    if 'email' in session:
        ut=session['ut']
        em=session['email']
        if ut=="medical":
            photo = check_photo(em)
            cur = make_connection()

            sql = "select * from medical where Email='" + em + "'"
            cur.execute(sql)
            n=cur.rowcount
            if n==1:
                data = cur.fetchone()
                return render_template("MedicalHome.html",data=data,photo=photo)
            else:
                return render_template("MedicalHome.html",msg="No Data Found")
        else:
            return redirect(url_for("autherror"))
    return redirect(url_for("login"))


@app.route('/change_medical_photo')
def change_medical_photo():
    if 'email' in session:
        ut=session['ut']
        em=session['email']
        if ut=='medical':
            photo = check_photo(em)
            cur = make_connection()
            sql = "delete from photos where email='"+em+"'"
            cur.execute(sql)
            n=cur.rowcount
            print(n)
            if n==1:
                os.remove("./static/photos/"+photo)
                return render_template("change_medical_photo.html",msg="Success")
            else:
                return render_template("change_medical_photo.html",msg="failure")
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))

@app.route('/medical_photo')
def medicalphoto():
    return render_template('photoupload_medical.html')

@app.route('/medical_photo1',methods=['GET','POST'])
def medicalphoto1():
    if 'email' in session:
        ut=session['ut']
        em=session['email']
        if ut=="medical":
            if request.method == 'POST':
                file = request.files['F1']
                if file:
                    path = os.path.basename(file.filename)
                    file_ext = os.path.splitext(path)[1][1:]
                    filename = str(int(time.time()))+'.'+file_ext
                    filename = secure_filename(filename)
                    cur = make_connection()
                    sql = "insert into photos values('"+em+"','"+filename+"')"
                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if n == 1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template('photoupload_medical1.html',result="success")
                        else:
                            return render_template('photoupload_medical1.html',result="Failure")
                    except:
                        return  render_template('photoupload_medical1.html',result="Duplicate")
                else:
                    return render_template('photoupload_medical.html')
            else:
                return redirect(url_for("autherror"))
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))
#---------------------------------------Admin Register----------------------------------------------------------
@app.route('/admin_reg',methods=['POST','GET'])
def admin_register():
    if 'email' in session:
        email=session['email']
        ut=session['ut']
        if ut=="admin":
            if request.method=='POST':
                try:

                    cur1 = make_connection()
                    cur2 = make_connection()

                    name = request.form['Name']
                    address = request.form['Address']
                    contact = request.form['Contact']
                    email = request.form['Email']
                    password = request.form['Password']
                    user_type = "admin"

                    sql1 = "insert into admin values('"+name+"','"+address+"','"+contact+"','"+email+"')"
                    sql2 = "insert into login values('"+email+"','"+password+"','"+user_type+"')"

                    cur1.execute(sql1)
                    cur2.execute(sql2)

                    n1 = cur1.rowcount
                    n2 = cur2.rowcount

                    if n1==1 and n2==1:
                        msg = "Admin Data Saved Successfully"
                    else:
                        msg = "Admin Data Not Saved Successfully"
                except psycopg2.err.IntegrityError:
                        msg = "User Already Exists"
                return render_template("admin_register.html",msg=msg)
            return render_template("admin_register.html")
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("login"))


@app.route('/show_admin')
def show_admin():
    if 'email' in session:
        email=session['email']
        ut=session['ut']
        if ut=="admin":
            cur1 = make_connection()
            sql = "select * from admin"
            cur1.execute(sql)
            n = cur1.rowcount
            if n>0:
                data = cur1.fetchall()
                return render_template("show_admin.html",data=data)
            else:
                msg = "No Admin Data Found"
                return render_template("show_admin.html",msg=msg)
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("login"))

@app.route('/update_admin_profile',methods=['POST','GET'])
def update_admin_profile():
    if 'email' in session:
        em=session['email']
        ut=session['ut']
        if ut=="admin":
            cur = make_connection()
            if request.method == "GET":
                sql = "select * from admin where Email='"+em+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    data=cur.fetchone()
                    return render_template("UpdateAdminProfile.html",data=data)
                else:
                    msg="profile not found"
                    return render_template("UpdateAdminProfile.html", msg=msg)
            else:
                name = request.form['name']
                address = request.form['address']
                contact = request.form['contact']

                sql = "update admin set Name='"+name+"',Address='"+address+"', Contact='"+contact+"' where Email='"+em+"'"
                cur.execute(sql)
                n = cur.rowcount
                if n==1:
                    msg="Profile Updated Successfully"
                else:
                    msg="Profile Not Updated Successfully"
                return render_template("UpdateAdminProfile.html",msg=msg)
        else:
            return redirect(url_for("/autherror"))
    else:
        return redirect(url_for("/login"))


@app.route('/search',methods=['POST','GET'])
def search():
    if request.method == "POST":
        cur = make_connection()
        m_name = request.form['mediname']
        sql = "select * from medical_medicine where Medicine_name like '%" + m_name + "%'"
        cur.execute(sql)
        n = cur.rowcount
        if n>0:
            data = cur.fetchall()
            return render_template("index.html",data=data)
        else:
            return render_template("index.html",msg="No Medicine Found")
    else:
        return render_template("index.html")


#-----------------------------------------Medical Register--------------------------------------------------------
@app.route('/medical_reg',methods=['POST','GET'])
def medical_reg():
    if 'email' in session:
        email=session['email']
        ut=session['ut']
        if ut=="admin":
            if request.method=='POST':
                try:
                    cur1 = make_connection()
                    cur2 = make_connection()

                    medical = request.form['Medical_name']
                    owner = request.form['Owner_name']
                    lic = request.form['Lic']
                    address = request.form['Address']
                    contact = request.form['Contact']
                    email = request.form['Email']
                    password = request.form['Password']
                    user_type = "medical"

                    sql1 = "insert into medical values('"+medical+"','"+owner+"','"+lic+"','"+address+"','"+contact+"','"+email+"')"
                    sql2 = "insert into login values('"+email+"','"+password+"','"+user_type+"')"

                    cur1.execute(sql1)
                    cur2.execute(sql2)

                    n1 = cur1.rowcount
                    n2 = cur2.rowcount

                    if n1==1 and n2==1:
                        msg = "Medical Data Saved Successfully"
                    else:
                        msg = "Medical Data Not Saved Successfully"
                    return render_template("medical_register.html",msg=msg)
                except psycopg2.err.IntegrityError:
                    msg = "User Already Exists"
                    return render_template("medical_register.html",msg=msg)
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("login"))


@app.route('/show_medical')
def show_medical():
    if 'email' in session:
        email=session['email']
        ut=session['ut']
        if ut=="admin":
            cur1 = make_connection()
            sql = "select * from medical"
            cur1.execute(sql)
            n = cur1.rowcount
            if n>0:
                data = cur1.fetchall()
                return render_template("show_medical.html",data=data)
            else:
                return render_template("show_medical.html",msg="No Medical Data Found")
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("login"))
@app.route('/show_all_medical')
def show_all_medical():
    cur1 = make_connection()
    sql = "select * from medical"
    cur1.execute(sql)
    n = cur1.rowcount
    if n>0:
        data = cur1.fetchall()
        return render_template("show_all_medical.html",data=data)
    else:
        return render_template("show_all_medical.html",msg="No Medical Data Found")
@app.route('/edit_medical',methods=['POST','GET'])
def edit_medical():
    if 'email' in session:
        email=session['email']
        ut=session['ut']
        if ut=="admin":
            if request.method=='POST':

                cur1 = make_connection()


                email = request.form['Email']

                sql = "select * from medical where Email='"+email+"'"

                cur1.execute(sql)
                n = cur1.rowcount

                if n==1:
                    data = cur1.fetchone()
                    return render_template("edit_medical.html",data=data)
                else:
                    return render_template("edit_medical.html",msg="No Medical Data Found")
            else:
                return render_template("show_medical.html")
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("login"))

@app.route('/update_medical',methods=['POST','GET'])
def update_medical():
    if 'email' in session:
        email=session['email']
        ut=session['ut']
        if ut=="admin":
            if request.method=='POST':

                cur1 = make_connection()


                Medical = request.form['Medical_name']
                Owner = request.form['Owner_name']
                Lic = request.form['Lic']
                Address = request.form['Address']
                Contact = request.form['Contact']
                Email = request.form['Email']

                sql = "update medical set Medical_name='"+Medical+"',Owner_name='"+Owner+"',Lic='"+Lic+"',Address='"+Address+"', Contact='"+Contact+"' where Email='"+Email+"'";

                cur1.execute(sql)
                n = cur1.rowcount

                if n==1:
                    msg="Data Updated Successfully"
                else:
                    msg = "Data Updated Failed"
                return render_template("edit_medical.html",msg=msg)
            else:
                return redirect("show_medical.html")
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("login"))


@app.route('/delete_medical',methods=['POST','GET'])
def delete_medical():
    if 'email' in session:
        email=session['email']
        ut=session['ut']
        if ut=="admin":
            if request.method=='POST':

                cur1 = make_connection()


                email = request.form['Email']

                sql = "select * from medical where Email='"+email+"'"

                cur1.execute(sql)
                n = cur1.rowcount

                if n==1:
                    data = cur1.fetchone()
                    return render_template("Delete_Medical.html",data=data)
                else:
                    return render_template("Delete_Medical.html",msg="No Medical Data Found")
            else:
                return redirect("show_medical")
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("login"))


@app.route('/deleted_medical',methods=['POST','GET'])
def deleted_medical():
    if 'email' in session:
        email=session['email']
        ut=session['ut']
        if ut=="admin":
            if request.method=='POST':

                cur1 = make_connection()


                Email = request.form['Email']

                sql = "delete from medical where Email='"+Email+"'"

                cur1.execute(sql)
                n = cur1.rowcount

                if n==1:
                    msg="Data Deleted Successfully"
                else:
                    msg = "Data Failed to Delete"
                return render_template("Delete_Medical.html",msg=msg)
            else:
                return redirect("show_medical")
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("login"))

@app.route('/update_medical_profile',methods=['POST','GET'])
def update_medical_profile():
    if 'email' in session:
        em=session['email']
        ut=session['ut']
        if ut=="medical":
            cur = make_connection()
            if request.method == "GET":
                sql = "select * from medical where Email='"+em+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    data=cur.fetchone()
                    return render_template("UpdateMedicalProfile.html",data=data)
                else:
                    msg="profile not found"
                    return render_template("UpdateMedicalProfile.html", msg=msg)
            else:
                 medical=request.form['medical_name']
                 owner=request.form['owner_name']
                 lic=request.form['lic']
                 address=request.form['address']
                 contact=request.form['contact']
                 sql = "update medical set Medical_name='"+medical+"',Owner_name='"+owner+"', Lic='"+lic+"',Address='"+address+"',Contact='"+contact+"' where Email='"+em+"'"
                 cur.execute(sql)
                 n = cur.rowcount
                 if n==1:
                     msg="Profile Updated Successfully"
                 else:
                     msg = "Profile Updated Failed"
                 return render_template("UpdateMedicalProfile.html",msg=msg)
        else:
            return redirect(url_for("/autherror"))
    else:
        return redirect(url_for("/login"))



#-----------------------------------------Change Password----------------------------------------------------------
@app.route('/changed_password', methods=['POST','GET'])
def changed_password():
    if 'email' in session:
        ut=session['ut']
        email=session['email']
        if ut=="admin":
            if request.method == 'POST':
                cur = make_connection()
                old_password = request.form['old_password']
                new_password = request.form['password']
                sql = "update login set Password='"+new_password+"' where Email='"+email+"' and Password='"+old_password+"'"

                cur.execute(sql)
                n = cur.rowcount
                if n == 1:
                   return render_template("AdminChangePassword.html", msg="Password Changed")
                else:
                    return render_template("AdminChangePassword.html", msg="Error!! Password doesn't Match")

            else:
                return render_template("AdminChangePassword.html")
        elif ut=="medical":
            if request.method == 'POST':
                cur = make_connection()
                old_password = request.form['old_password']
                new_password = request.form['password']
                sql = "update login set Password='"+new_password+"' where Email='"+email+"' and Password='"+old_password+"'"

                cur.execute(sql)
                n = cur.rowcount
                if n == 1:
                   return render_template("MedicalChangePassword.html", msg="Password Changed")
                else:
                    return render_template("MedicalChangePassword.html", msg="Error!! Password doesn't Match")

            else:
                return render_template("MedicalChangePassword.html")
        else:
            return redirect("autherror")
    else:
        return redirect("login")

#----------------------------------------Medicine---------------------------------
@app.route('/medicine_reg',methods=['POST','GET'])
def medicine_reg():
    if 'email' in session:
        em = session['email']
        ut = session['ut']
        if request.method == "GET":
            return render_template("MedicineReg.html")
        else:
            if ut=="medical":
                if request.method == 'POST':
                    try:
                        cur = make_connection()
                        id = 0
                        medicine_name=request.form['medicine_name']
                        medicine_type=request.form['medicine_type']
                        medicine_lic=request.form['medicine_lic']
                        medicine_price =request.form['medicine_price']
                        medicine_description=request.form['medicine_description']

                        sql = "INSERT INTO medicine (med_id, medicine_name, medicine_type, medicine_lic, medicine_price, medicine_description, Email_of_medical) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        values = (id, medicine_name, medicine_type, medicine_lic, medicine_price, medicine_description,em)
                        cur.execute(sql, values)

                        n=cur.rowcount
                        if n==1:
                            msg = "Medicine Registered Successfully"
                        else:
                            msg = "Medicine Registered Failed"
                        return render_template("MedicineReg.html",msg=msg)
                    except psycopg2.err.IntegrityError:
                        msg = "Medicine already Registered"
                        return render_template("MedicineReg.html",msg=msg)
                else:
                    return redirect(url_for("autherror"))
            else:
                return redirect(url_for("autherror"))
    else:
        return redirect("login")

@app.route('/show_medicine')
def show_medicine():
    if 'email' in session:
        em=session['email']
        ut = session['ut']
        if ut=="medical":
            cur = make_connection()
            sql = "select * from medicine where Email_of_medical='"+em+"'"
            cur.execute(sql)
            n = cur.rowcount
            if n>0:
                data=cur.fetchall()
                return render_template("ShowMedicine.html", data=data)
            else:
                return render_template("ShowMedicine.html", msg="Data Not Found")
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect("login")


@app.route('/edit_medicine',methods=['POST','GET'])
def edit_medicine():
    if 'email' in session:
        em = session['email']
        ut = session['ut']
        if ut=="medical":
            if request.method == 'POST':
                cur = make_connection()
                id = request.form['T1']
                sql = "select * from medicine where med_id='"+id+"'"
                cur.execute(sql)
                n = cur.rowcount
                if n==1:
                    data = cur.fetchone()
                    return render_template("EditMedicine.html",data=data)
                else:
                    return render_template("EditMedicine.html",msg="Medicine Not Found")
            else:
                return redirect(url_for("show_medicine"))
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("login"))

@app.route('/update_medicine',methods=['POST','GET'])
def update_medicine():
    if 'email' in session:
        em=session['email']
        ut = session['ut']
        if ut=='medical':
            if request.method == "POST":
                cur = make_connection()
                id = request.form['T1']
                medicine_name = request.form['medicine_name']
                medicine_type = request.form['medicine_type']
                medicine_lic = request.form['medicine_lic']
                medicine_price = request.form['medicine_price']
                medicine_description = request.form['medicine_description']

                sql = "update medicine set Medicine_name='"+medicine_name+"',Medicine_type='"+medicine_type+"',Medicine_lic='"+medicine_lic+"',Medicine_price='"+medicine_price+"',Medicine_description='"+medicine_description+"' where med_id='"+id+"'"
                cur.execute(sql)
                n = cur.rowcount
                if n==1:
                    return render_template('UpdateMedicine.html',msg="Medicine Updated Successfully")
                else:
                    return render_template('UpdateMedicine.html',msg="Medicine Updated Failed")
            else:
                return redirect(url_for("show_medicine"))
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("login"))

@app.route('/delete_medicine',methods=['POST','GET'])
def delete_medicine():
    if 'email' in session:
        em = session['email']
        ut = session['ut']
        if ut=="medical":
            if request.method == 'POST':
                cur = make_connection()
                id = request.form['T1']
                sql = "select * from medicine where med_id='"+id+"'"
                cur.execute(sql)
                n = cur.rowcount
                if n==1:
                    data = cur.fetchone()
                    return render_template("DeleteMedicine.html",data=data)
                else:
                    return render_template("DeleteMedicine.html",msg="Medicine Not Found")
            else:
                return redirect(url_for("show_medicine"))
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("login"))
@app.route('/deleted_medicine',methods=['POST','GET'])
def deleted_medicine():
    if 'email' in session:
        em = session['email']
        ut = session['ut']
        if ut=="medical":
            if request.method=='POST':
                cur1 = make_connection()
                id = request.form['T1']
                sql = "delete from medicine where med_id='"+id+"'"
                cur1.execute(sql)
                n = cur1.rowcount
                if n==1:
                    msg="Medicine Deleted Successfully"
                else:
                    msg = "Medicine Failed to Delete"
                return render_template("DeletedMedicine.html",msg=msg)
            else:
                return redirect("show_medicine")
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("login"))




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
