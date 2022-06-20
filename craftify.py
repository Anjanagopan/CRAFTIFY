from flask import Flask, render_template, request, session, jsonify
from DBConnection import Db

app = Flask(__name__)
app.secret_key="h1"



@app.route('/')
def launching():
    return render_template('admin/main_index.html')

@app.route('/login')
def login():
    return render_template('admin/login_index.html')

@app.route('/login_post', methods=['post'])
def login_post():
   db=Db()
   uname = request.form['textfield']
   password = request.form['textfield2']
   ss=db.selectOne("select * from login WHERE username='"+uname+"'and password='"+password+"'")
   if ss is not None:
       session['lid']=ss['login_id']
       if ss ['type']=='admin':

            return render_template('admin/admin_index.html')
       # elif ss ['type']=='seller':
       #      return view_registered_seller_post
       # elif ss ['type']=='user':
       #      return view_users_post
       else:
            return '''<script>alert('Invalid User!');window.location='/login'</script>'''
   else:
       return '''<script>alert('Invalid User!');window.location='/login'</script>'''

@app.route('/package_management')
def package_management():
    return render_template('admin/package_management.html')

@app.route('/package_management_post', methods=['post'])
def package_management_post():
    db = Db()
    packagename = request.form['textfield']
    amount = request.form['textfield2']
    details = request.form['textfield3']

    db.insert("insert into package_model (p_name,p_amount,p_details) VALUES ('"+packagename+"','"+amount+"','"+details+"')")

    return 'ok..Packages added successfully'

@app.route('/exhibition_management')
def exhibition_management():
    return render_template('admin/exhibition_management.html')

@app.route('/exhibition_management_post', methods=['post'])
def exhibition_management_post():
    db = Db()
    exhibitionname = request.form['textfield']
    exhibitiondate = request.form['textfield2']
    starttime = request.form['textfield3']
    endtime = request.form['textfield4']
    db.insert("insert into exhibition_model (e_name,e_date,e_starttime,e_endtime) VALUES ('"+exhibitionname+"','"+exhibitiondate+"','"+starttime+"','"+endtime+"')")

    return 'ok..Exhibition added successfully'


@app.route('/view_approved_seller')
def view_approved_seller():
    db = Db()
    res = db.select("SELECT * FROM `login`,`seller_model` WHERE `seller_model`.`login_id`=`login`.`login_id` AND login.type = 'seller'")
    return render_template('admin/view_approved_seller.html',data = res)

@app.route('/view_approved_seller_post', methods=['post'])
def view_approved_seller_post():
    db = Db()
    sellername = request.form['textfield']
    res = db.select("SELECT * FROM `login`,`seller_model` WHERE `seller_model`.`login_id`=`login`.`login_id` AND login.type = 'seller' and  seller_model.s_name='"+sellername+"' ")
    print(res)
    return render_template('admin/view_approved_seller.html',data = res)

@app.route('/approve_seller/<s_id>')
def approve_seller(s_id):
    db = Db()
    db.update("update login set type = 'seller' where login_id = '"+str(s_id)+"'")
    return '''<script>alert('approved');window.location='/view_registered_seller'</script>'''

@app.route('/block_approved_seller/<s_id>')
def block_approved_seller(s_id):
    db = Db()
    print(s_id)
    db.update("update login set type = 'blocked' where login_id = '"+s_id+"'")
    return '''<script>alert('blocked');window.location='/view_registered_seller'</script>'''



@app.route('/view_packages')
def view_packages():
    db = Db()
    res = db.select("select * from package_model")
    print(res)
    return render_template('admin/view_packages.html', data=res)


@app.route('/view_package_post', methods=['post'])
def view_package_post():
    db = Db()
    res = db.select("select * from package_model")
    print(res)
    return render_template('admin/view_packages.html', data=res)

@app.route('/delete_package/<package_id>')
def delete_package(package_id):
    d = Db()
    qry = "delete from package_model where package_id='"+package_id+"'"
    res = d.delete(qry)
    return '''<script>alert('Deleted');window.location='/view_packages'</script>'''

@app.route('/edit_package/<package_id>')
def edit_package(package_id):
    d = Db()
    qry = "SELECT * FROM `package_model` WHERE `package_id`='"+str(package_id)+"'"
    res=d.selectOne(qry)
    return render_template('admin/edit_package.html',data=res)

@app.route('/edit_package_post', methods=['post'])
def edit_package_post():
    id=request.form['p_id']
    name=request.form['textfield']
    amount=request.form['textfield2']
    details=request.form['textfield3']
    d = Db()
    qry = "UPDATE package_model SET p_name='"+name+"',p_amount='"+amount+"',p_details='"+details+"' where package_id='"+str(id)+"' "
    res = d.update(qry)

    return '''<script>alert('updated');window.location='/view_packages'</script>'''

@app.route('/view_exhibition')
def view_exhibition():
    db = Db()
    res = db.select("select * from exhibition_model")
    print(res)
    return render_template('admin/view_exhibition.html', data=res)


@app.route('/view_exhibition_post', methods=['post'])
def view_exhibition_post():
    db = Db()
    res = db.select("select * from exhibition_model")
    print(res)
    return render_template('admin/view_exhibition.html', data=res)


@app.route('/edit_exhibition/<exhibition_id>')
def edit_exhibition(exhibition_id):
    d = Db()
    qry = "SELECT * FROM `exhibition_model` WHERE `exhibition_id`='"+str(exhibition_id)+"'"
    res=d.selectOne(qry)
    return render_template('admin/edit_exhibition.html',data=res)

@app.route('/edit_exhibition_post', methods=['post'])
def edit_exhibition_post():
    id=request.form['e_id']
    exhibitionname=request.form['textfield']
    exhibitiondate=request.form['textfield2']
    starttime = request.form['textfield3']
    endtime = request.form['textfield4']
    d = Db()
    qry = "UPDATE exhibition_model SET e_name='"+exhibitionname+"',e_date='"+exhibitiondate+"',e_starttime='"+starttime+"',e_endtime='"+endtime+"' where exhibition_id='"+str(id)+"' "
    res = d.update(qry)

    return '''<script>alert('updated');window.location='/view_exhibition'</script>'''

@app.route('/delete_exhibition/<exhibition_id>')
def delete_exhibition(exhibition_id):
    d = Db()
    qry = "delete from exhibition_model where exhibition_id='"+exhibition_id+"'"
    res = d.delete(qry)
    return '''<script>alert('Deleted');window.location='/view_exhibition'</script>'''


@app.route('/view_and_add_wiiner/<exhid>')
def view_and_add_wiiner(exhid):
    q="SELECT `exhition_request`.*,`seller_model`.* FROM `exhition_request` INNER JOIN `seller_model` ON `exhition_request`.`ulid`=`seller_model`.`login_id` WHERE `exhition_request`.`exibitionid`='"+exhid+"' and exhition_request.status='approved'"
    d=Db()
    r=d.select(q)

    print("--------------------",q)

    win="SELECT `winner_model`.*,`seller_model`.* FROM `winner_model` INNER JOIN `seller_model` ON `winner_model`.`sellerlid`=`seller_model`.`login_id` WHERE `winner_model`.`exhibition_id`='"+exhid+"'"
    c=Db()
    winners=c.select(win)
    return render_template('admin/view_participents.html',data=r,exhid=exhid,winn=winners)
@app.route('/view_ratings/<pid>')
def view_ratings(pid):
    q="SELECT `rating_model`.*,`user_model`.* FROM `rating_model` INNER JOIN `user_model` ON `rating_model`.`ulid`=`user_model`.`login_id` WHERE `rating_model`.`pid`='"+pid+"'"
    d=Db()
    res=d.select(q)
    return render_template('admin/View_rating.html',data=res)
@app.route('/add_winners/<sellerid>/<exhid>')
def add_winners(sellerid,exhid):
    q="INSERT INTO `winner_model`(`exhibition_id`,`w_date`,`sellerlid`)VALUES('"+exhid+"',curdate(),'"+sellerid+"')"
    d=Db()
    res=d.insert(q)
    return view_and_add_wiiner(exhid)

@app.route('/delete_wiiners/<winnerid>/<exhid>')
def delete_wiiners(winnerid,exhid):
    q="DELETE FROM `winner_model` WHERE `winner_id`='"+winnerid+"'"
    d=Db()
    res=d.select(q)
    return view_and_add_wiiner(exhid)


@app.route('/admin_view_exhibtionreq/<exid>')
def admin_view_exhibtionreq(exid):
    q="SELECT `exhition_request`.*,`seller_model`.*,`product_model`.* FROM `exhition_request` INNER JOIN `product_model` ON `exhition_request`.`productid`=`product_model`.`product_id` INNER JOIN `seller_model` ON `product_model`.`seller_id`=`seller_model`.`login_id` where `exhition_request`.`exibitionid`='"+exid+"' and exhition_request.status='pending'"
    d=Db()
    res=d.select(q)
    return render_template('admin/view_echibhition_request_and_approve.html',data=res,exid=exid)
@app.route('/admin_approve_requust/<reqid>/<exid>')
def admin_approve_requust(reqid,exid):
    q="UPDATE `exhition_request` SET `status`='approved' WHERE `rid`='"+reqid+"'"
    d=Db()
    res=d.update(q)
    return admin_view_exhibtionreq(exid)

@app.route('/admin_reject_requust/<reqid>/<exid>')
def admin_reject_requust(reqid,exid):
    q="UPDATE `exhition_request` SET `status`='rejected' WHERE `rid`='"+reqid+"'"
    d=Db()
    res=d.update(q)
    return admin_view_exhibtionreq(exid)

@app.route('/admin_view_approved_exhibtion/<exid>')
def admin_view_approved_exhibtion(exid):
    q="SELECT `exhition_request`.*,`seller_model`.*,`product_model`.* FROM `exhition_request` INNER JOIN `product_model` ON `exhition_request`.`productid`=`product_model`.`product_id` INNER JOIN `seller_model` ON `product_model`.`seller_id`=`seller_model`.`login_id` where `exhition_request`.`exibitionid`='"+exid+"' and exhition_request.status='approved'"
    d=Db()
    res=d.select(q)
    return render_template('admin/view_approved_ex_request.html',data=res)

@app.route('/view_products')
def view_products():
    db = Db()
    res = db.select("select * from product_model ")
    print(res)
    qry2="SELECT * FROM `seller_model`"
    res2=db.select(qry2)
    return render_template('admin/view_products.html',data=res,data2=res2)

@app.route('/view_products_post', methods=['post'])
def view_products_post():
    db = Db()
    btn=request.form['button']
    print("===",btn)
    if btn=="Check":
        sid = request.form['sss']
        q="select * from product_model WHERE seller_id='"+sid+"'"
        r=db.select(q)
        print(q)
        return render_template('admin/view_products.html',data = r)
    if btn=="Search":
        productname = request.form['textfield']
        res = db.select("select * from product_model WHERE product_name='" + productname + "' ")
        print(res)
        return render_template('admin/view_products.html', data=res)


@app.route('/view_approved_seller_product/<v>')
def view_approved_seller_product(v):
    db = Db()
    res = db.select("select * from product_model where `seller_id`='"+v+"'")
    print(res)
    return render_template('admin/view_approved_seller_product.html', data=res)

@app.route('/view_approved_seller_product_post', methods=['post'])
def view_approved_seller_product_post():
    db = Db()
    productname = request.form['textfield']
    res = db.select("select * from product_model WHERE product_name='" + productname + "' ")
    print(res)
    return render_template('admin/view_approved_seller_product.html',data = res)


@app.route('/view_rejected_seller')
def view_rejected_seller():
    db = Db()
    res = db.select("SELECT * FROM `login`,`seller_model` WHERE `seller_model`.`login_id`=`login`.`login_id` AND login.type = 'reject'")
    return render_template('admin/view_rejected_seller.html',data = res)

@app.route('/view_rejected_seller_post', methods=['post'])
def view_rejected_seller_post():
    db = Db()
    sellername = request.form['textfield']
    res = db.select("SELECT * FROM `login`,`seller_model` WHERE `seller_model`.`login_id`=`login`.`login_id` AND login.type = 'reject' and seller_model.s_name='" + sellername + "' ")
    print(res)
    return render_template('admin/view_rejected_seller.html',data = res)

@app.route('/reject_seller/<s_id>')
def reject_seller(s_id):
    db = Db()
    print(s_id)
    db.update("update login set type = 'reject' where login_id = '"+s_id+"'")
    return '''<script>alert('rejected');window.location='/view_registered_seller'</script>'''


@app.route('/view_registered_seller')
def view_registered_seller():
    db = Db()
    res = db.select("SELECT `seller_model`.*, `login`.`type` FROM `login` INNER JOIN `seller_model` ON `seller_model`.`login_id`=`login`.`login_id` WHERE `login`.`type`='pending' ")

    print(res)
    return render_template('admin/view_registered_seller.html', data=res)


@app.route('/view_registered_seller_post', methods=['post'])
def view_registered_seller_post():
    db = Db()
    sellername = request.form['textfield']
    res = db.select("select * from seller_model WHERE s_name='" + sellername + "' ")
    print(res)
    return render_template('admin/view_registered_seller.html',data = res)



@app.route('/view_users')
def view_users():
    db = Db()
    res = db.select("select * from user_model ")
    print(res)
    return render_template('admin/view_users.html', data=res)

@app.route('/view_users_post', methods=['post'])
def view_users_post():
    db = Db()
    username = request.form['textfield']
    res = db.select("select * from user_model WHERE u_name='" + username + "' ")
    print(res)
    return render_template('admin/view_users.html',data = res)



@app.route('/view_profit')
def view_profit():
    db = Db()
    # res = db.select("SELECT `user_model`.*,`package_model`.`p_name`,`package_model`.`p_amount`, `profit_model`.`amount`,`profit_model`.`date`,`profit_model`.`type` FROM `profit_model` INNER JOIN `user_model` ON `user_model`.`login_id`=`profit_model`.`user_id` INNER JOIN `buy_model` ON `buy_model`.`buy_id`=`profit_model`.`buy_id` INNER JOIN `package_model` ON `package_model`.`package_id`=`buy_model`.`package_id`  WHERE `buy_model`.`type`='subscription' UNION(SELECT `user_model`.*,`product_model`.`product_name` AS p_name,`product_model`.`product_price` AS `p_amount`, `profit_model`.`amount`,`profit_model`.`date`,`profit_model`.`type` FROM `profit_model` INNER JOIN `user_model` ON `user_model`.`login_id`=`profit_model`.`user_id` INNER JOIN `buy_model` ON `buy_model`.`buy_id`=`profit_model`.`buy_id` INNER JOIN `product_model` ON `product_model`.`product_id`=`buy_model`.`package_id`  WHERE `buy_model`.`type`='sales')")
    res = db.select("SELECT `user_model`.*,`package_model`.`p_name`,`package_model`.`p_amount`, `profit_model`.`amount`,`profit_model`.`date`,`profit_model`.`type` FROM `profit_model` INNER JOIN `user_model` ON `user_model`.`login_id`=`profit_model`.`user_id` INNER JOIN `buy_model` ON `buy_model`.`buy_id`=`profit_model`.`buy_id` INNER JOIN `package_model` ON `package_model`.`package_id`=`buy_model`.`package_id`  WHERE `buy_model`.`type`='subscription' UNION(SELECT `user_model`.*,`product_model`.`product_name` AS p_name,`product_model`.`product_price` AS `p_amount`, `profit_model`.`amount`,`profit_model`.`date`,`profit_model`.`type` FROM `profit_model` INNER JOIN `user_model` ON `user_model`.`login_id`=`profit_model`.`user_id` INNER JOIN `buy_model` ON `buy_model`.`buy_id`=`profit_model`.`buy_id` INNER JOIN `product_model` ON `product_model`.`product_id`=`buy_model`.`package_id`  WHERE `buy_model`.`type`='sales')")
    print(res)
    return render_template('admin/view_profit.html', data=res)

@app.route('/view_profit_post', methods=['post'])
def view_profit_post():
    db = Db()
    res = db.select("select * from profit_model ")
    print(res)
    return render_template('admin/view_profit.html',data = res)


@app.route('/home')
def home():
    return render_template('admin/home.html')




# -----------------------------templates--------------------------------------------

@app.route('/admin_index')
def admin_index():
    return render_template('admin/admin_index.html')


@app.route('/admin_index_post', methods=['post'])
def admin_index_post():
    return render_template('admin/admin_index.html')

@app.route("/and_login",methods=['post'])
def androidlogin():

    username=request.form["uname"]
    password=request.form["pswd"]

    db=Db()

    qry="SELECT * FROM login WHERE `username`='"+username+"' AND `password`='"+password+"'"
    print(qry)
    # return jsonify(status='no')
    res=db.selectOne(qry)
    print(qry)
    if res is not None:
        if res["type"]=="seller":
            return jsonify(status='ok',lid=res['login_id'],type=res['type'])
        elif  res["type"]=="user":
            sb="SELECT * FROM `buy_model` WHERE `user_lid`='"+str(res['login_id'])+"' AND `status`='active'"
            dd=Db()
            r=dd.selectOne(sb)

            if r is not None:

                

                return jsonify(status='ok', lid=res['login_id'], type=res['type'],sub="yes",day="noexeed")
            else:
                return jsonify(status='ok', lid=res['login_id'], type=res['type'],sub="no",day="")

    else:
        return jsonify(status='no')

@app.route("/and_signup",methods=['post'])
def andsignup():
    db=Db()
    s_name=request.form["name"]
    s_gender=request.form['gender']
    s_place=request.form['district']
    s_post=request.form['post']
    s_pincode=request.form['pin']
    s_email = request.form['email']
    s_phone = request.form['phone']
    s_image=request.files['image']
    password=request.form['password']
    import time
    timestr = time.strftime("%Y%m%d-%H%M%S")
    path="C:\\Users\\user\\PycharmProjects\\craftify\\static\\seller\\"+timestr+".jpg"
    s_image.save(path)

    filename="/static/seller/"+timestr+".jpg"

    qry="INSERT INTO login (`username`,`password`,`type`) VALUES('"+s_email+"','"+password+"','pending')"
    lid=db.insert(qry)

    qry="INSERT INTO `seller_model` (`s_name`,`s_gender`,`s_place`,`s_post`,`s_pincode`,`s_email`,`s_phone`,`s_image`,`login_id`) VALUES ('"+s_name+"','"+s_gender+"','"+s_place+"','"+s_post+"','"+s_pincode+"','"+s_email+"','"+s_phone+"','"+filename+"','"+str(lid)+"')"
    res=db.insert(qry)
    print(res)
    return jsonify(status='ok')



@app.route("/and_updateprofile",methods=['post'])
def and_updateprofile():
    db=Db()
    s_name=request.form["name"]
    s_gender=request.form['gender']
    s_place=request.form['district']
    s_post=request.form['post']
    s_pincode=request.form['pin']
    s_email = request.form['email']
    s_phone = request.form['phone']
    s_image=request.files['image']
    import time
    timestr = time.strftime("%Y%m%d-%H%M%S")
    path="C:\\Users\\user\\PycharmProjects\\craftify\\static\\seller\\"+timestr+".jpg"
    s_image.save(path)

    filename="/static/seller/"+timestr+".jpg"

    qry = "UPDATE seller_model SET  s_name='"+s_name+"',s_gender='"+s_gender+"',s_place='"+s_place+"',s_post='"+s_post+"',s_pincode='"+s_pincode+"',s_email ='"+s_email+"',s_phone='"+s_phone+"' "
    db.update(qry)

    return jsonify(status='ok')





@app.route("/and_view_profile",methods=['post'])
def and_view_profile():
    lid=request.form["lid"]
    qry="SELECT * FROM `seller_model` WHERE `login_id`='"+lid+"'"
    db=Db()
    res=db.selectOne(qry)
    return jsonify(status='ok',data=res)



@app.route("/and_view_products",methods=['post'])
def and_view_products():
    lid=request.form["lid"]
    qry="SELECT * FROM `product_model` WHERE `seller_id`='"+lid+"'"
    db=Db()
    res=db.select(qry)
    return jsonify(status='ok',data=res)
@app.route("/andaddproducts",methods=['post'])
def andaddproducts():
    db=Db()
    name=request.form["name"]
    count=request.form['count']
    details=request.form['details']
    price=request.form['price']
    lid=request.form['lid']

    s_image=request.files['image']
    import time
    timestr = time.strftime("%Y%m%d-%H%M%S")
    path="C:\\Users\\user\\PycharmProjects\\craftify\\static\\sellerproduct\\"+timestr+".jpg"
    s_image.save(path)

    filename="/static/sellerproduct/"+timestr+".jpg"

    qry="INSERT INTO `product_model` (`product_name`,`product_count`,`product_price`,`product_details`,`photo`,`seller_id`) VALUES ('"+name+"','"+count+"','"+price+"','"+details+"','"+filename+"','"+lid+"')"
    db.insert(qry)

    return jsonify(status='ok')



@app.route("/andaddproducts",methods=['post'])
def andaddprodccucts():
    db=Db()
    name=request.form["title"]
    count=request.form['count']
    details=request.form['details']
    price=request.form['price']
    lid=request.form['lid']

    s_image=request.files['image']
    import time
    timestr = time.strftime("%Y%m%d-%H%M%S")
    path="C:\\Users\\user\\PycharmProjects\\craftify\\static\\sellerproduct\\"+timestr+".jpg"
    s_image.save(path)

    filename="/static/sellerproduct/"+timestr+".jpg"

    qry="INSERT INTO `product_model` (`product_name`,`product_count`,`product_price`,`product_details`,`photo`,`seller_id`) VALUES ('"+name+"','"+count+"','"+price+"','"+details+"','"+filename+"','"+lid+"')"
    db.insert(qry)

    return jsonify(status='ok')



@app.route("/andaddvedios",methods=['post'])
def andaddvedios():
    db=Db()
    # video_name=request.form["video_name"]
    title=request.form['title']
    description=request.form['description']
    lid=request.form['lid']

    s_image=request.files['image']
    import time
    timestr = time.strftime("%Y%m%d-%H%M%S")
    path="C:\\Users\\user\\PycharmProjects\\craftify\\static\\tutorial\\"+s_image.filename
    s_image.save(path)

    filename="/static/tutorial/"+s_image.filename
    qry="INSERT INTO `tutorial_model`(title,`description`,`v_date`,`seller_id`,path) VALUES ('"+title+"','"+description+"',CURDATE(),'"+lid+"','"+filename+"')"
    db.insert(qry)

    return jsonify(status='ok')


@app.route("/and_view_tutorial",methods=['post'])
def and_view_tutorial():
    db=Db()

    lid=request.form['lid']



    qry="select * from `tutorial_model` where `seller_id`='"+lid+"'"
    res=db.select(qry)

    return jsonify(status='ok',data=res)

@app.route("/and_view_exhibition",methods=['post'])
def and_view_exhibition():
    db=Db()



    qry="select * from `exhibition_model` where e_date>curdate() "
    res=db.select(qry)

    return jsonify(status='ok',data=res)


@app.route("/and__apply_exhibition",methods=['post'])
def and_apply_exhibition():
    db=Db()

    lid=request.form['lid']
    exid=request.form['exid']
    pid=request.form["pid"]

    qry="INSERT INTO `exhition_request`(ulid,exibitionid,`date`,`status`,productid) VALUES ('"+lid+"','"+exid+"',curdate(),'pending','"+pid+"')"

    res=db.insert(qry)

    return jsonify(status='ok')


@app.route("/and_view_winner",methods=['post'])
def and_view_winner():
    db=Db()

    qry="select * from `winner_model` "
    res=db.select(qry)

    return jsonify(status='ok',data=res)


@app.route("/and_view_booking",methods=['post'])
def and_view_booking():
    db=Db()

    qry="select * from `master_model` "
    res=db.select(qry)

    return jsonify(status='ok',data=res)


@app.route("/and_view_rating",methods=['post'])
def and_view_rating():
    db=Db()
    pid=request.form["pid"]

    qry="SELECT `rating_model`.*,`user_model`.`u_name` FROM `rating_model` INNER JOIN `user_model` ON `rating_model`.`ulid`=`user_model`.`login_id` where rating_model.pid='"+pid+"' "
    res=db.select(qry)

    return jsonify(status='ok',data=res)
@app.route('/and_view_winners',methods=["post"])
def and_view_winners():

    exhid=request.form["exb"]
    q="SELECT `winner_model`.*,`seller_model`.* FROM `winner_model` INNER JOIN `seller_model` ON `winner_model`.`sellerlid`=`seller_model`.`login_id` WHERE `winner_model`.`exhibition_id`='"+exhid+"'"
    d=Db()
    res=d.selectOne(q)
    if res is not None:
        return jsonify(status="ok",name=res["s_name"],img=res["s_image"])
    else:
        return jsonify(status="no")
@app.route('/and_view_bookings',methods=["post"])
def and_view_bookings():
    selleid=request.form["lid"]
    q="SELECT `master_model`.*,`product_model`.*,`user_model`.* FROM `master_model` INNER JOIN `product_model` ON `master_model`.`product_id`=`product_model`.`product_id` INNER JOIN `user_model` ON `master_model`.`user_id`=`user_model`.`login_id` WHERE `product_model`.`seller_id`='"+selleid+"'"
    d=Db()
    res=d.select(q)
    return jsonify(status="ok",data=res)
@app.route('/seller_update_booking_status',methods=["post"])
def seller_update_booking_status():
    mid=request.form["mid"]
    q="UPDATE `master_model` SET `status`='completed' WHERE `master_id`='"+mid+"'"
    d=Db()
    res=d.update(q)
    return jsonify(status="ok",data=res)
@app.route('/seller_view_req_status',methods=["post"])
def seller_view_req_status():
    lid=request.form["lid"]
    q="SELECT `exhition_request`.*,`product_model`.* ,`exhibition_model`.* FROM `exhition_request` INNER JOIN `product_model` ON `exhition_request`.`productid`=`product_model`.`product_id` INNER join `exhibition_model` ON `exhibition_model`.`exhibition_id`=`exhition_request`.`exibitionid` WHERE `ulid`='"+lid+"'"
    d=Db()
    res=d.select(q)
    return jsonify(status="ok",data=res)
#________________________________--user--------------------------------------------------


@app.route("/and_user_signup",methods=['post'])
def and_user_signup():
    db=Db()
    s_name=request.form["name"]
    s_gender=request.form['gender']
    s_place=request.form['district']
    s_post=request.form['post']
    s_pincode=request.form['pin']
    s_email = request.form['email']
    s_phone = request.form['phone']
    s_image=request.files['image']
    password=request.form['password']
    import time
    timestr = time.strftime("%Y%m%d-%H%M%S")
    path="C:\\Users\\user\\PycharmProjects\\craftify\\static\\userimg\\"+timestr+".jpg"
    s_image.save(path)

    filename="/static/userimg/"+timestr+".jpg"

    qry="INSERT INTO login (`username`,`password`,`type`) VALUES('"+s_email+"','"+password+"','user')"
    lid=db.insert(qry)

    qry="INSERT INTO `user_model`(`u_name`,`u_gender`,`u_email`,`u_phone`,`u_place`,`u_post`,`u_pincode`,`image`,`login_id`,`reg_date`)VALUES('"+s_name+"','"+s_gender+"','"+s_email+"','"+s_phone+"','"+s_place+"','"+s_post+"','"+s_pincode+"','"+filename+"','"+str(lid)+"',curdate())"
    res=db.insert(qry)
    print(res)
    return jsonify(status='ok')


@app.route("/and_user_view_profile",methods=['post'])
def and_user_view_profile():
    lid=request.form["lid"]
    qry="SELECT * FROM `user_model` WHERE `login_id`='"+lid+"'"
    db=Db()
    res=db.selectOne(qry)
    return jsonify(status='ok',data=res)



@app.route('/and_user_view_packages',methods=["post"])
def and_user_view_packages():
    q="SELECT * FROM `package_model`"
    d=Db()
    res=d.select(q)
    return jsonify(status="ok",data=res)

@app.route('/and_package_buy',methods=["post"])
def and_package_buy():
    amount = request.form["total"]
    bank = request.form["bank"]
    pin = request.form["accpin"]
    lid = request.form["lid"]
    pkid = request.form["pid"]
    d=Db()

    check="SELECT * FROM `buy_model` WHERE `user_lid`='' AND `status`='active'"
    f=Db()
    r=f.selectOne(check)
    if r is None:

        bank_check = "SELECT `amount` FROM bank WHERE bank='" + bank + "' AND accpin='" + pin + "'"
        bres = d.selectOne(bank_check)
        if int(bres["amount"]) > int(amount):
            dd = Db()
            profitamount=amount

            qq="INSERT INTO `payment_model`(`ulid`,`amount`,`date`)VALUES('"+lid+"','"+amount+"',curdate())"
            payid=dd.insert(qq)

            q="INSERT INTO `buy_model`(`buy_date`,`package_id`,`type`,`user_lid`,`total`,`status`,paymentid)VALUES(CURDATE(),'"+pkid+"','subscription','"+lid+"','"+str(profitamount)+"','active','"+str(payid)+"')"
            buyid=dd.insert(q)

            prof="INSERT INTO profit_model (`type`,`amount`,`date`,`user_id`,`buy_id`) VALUES ('subscription','"+str(profitamount)+"',curdate(),'"+lid+"','"+str(buyid)+"')"
            dd.insert(prof)
            bankqry = "UPDATE bank SET amount=amount-'" + amount + "' WHERE bank='" + bank + "' AND `accpin`='" + pin + "'"
            dd.update(bankqry)


            return jsonify(status="ok")
        else:
            return jsonify(status="low")
    else:
        return jsonify(status="exist")

@app.route('/user_view_tutorials',methods=["post"])
def user_view_tutorials():
    q="SELECT `seller_model`.*,`tutorial_model`.* FROM `seller_model` INNER JOIN `tutorial_model` ON `seller_model`.`login_id`=`tutorial_model`.`seller_id`"
    d=Db()
    resd=d.select(q)
    return jsonify(status="ok",data=resd)

@app.route("/and_user_view_exhibition",methods=['post'])
def and_user_view_exhibition():
    db=Db()
    qry="select * from `exhibition_model` where e_date=curdate() "
    res=db.select(qry)

    return jsonify(status='ok',data=res)

@app.route("/and_user_view_exhibition_product",methods=['post'])
def and_user_view_exhibition_product():
    db=Db()

    exid=request.form["exhid"]

    qry="SELECT `seller_model`.*,`product_model`.*,`exhition_request`.* FROM `exhition_request` INNER JOIN `product_model` ON `exhition_request`.`productid`=`product_model`.`product_id` INNER JOIN `seller_model` ON `product_model`.`seller_id`=`seller_model`.`login_id` WHERE `exhition_request`.`exibitionid`='"+exid+"' AND `exhition_request`.`status`='approved'"
    res=db.select(qry)

    return jsonify(status='ok',data=res)




@app.route('/and_product_buy',methods=["post"])
def and_product_buy():
    amount = request.form["total"]
    bank = request.form["bank"]
    pin = request.form["accpin"]
    lid = request.form["lid"]
    pid = request.form["pid"]
    sellerid = request.form["selerid"]
    name = request.form["name"]
    phone = request.form["phone"]
    place = request.form["place"]
    post = request.form["post"]
    pincode = request.form["pincode"]
    nearplace = request.form["nearplace"]
    d=Db()
    bank_check = "SELECT `amount` FROM bank WHERE bank='" + bank + "' AND accpin='" + pin + "'"
    bres = d.selectOne(bank_check)
    if float(bres["amount"]) > float(amount):
        dd = Db()

        qq="INSERT INTO `payment_model`(`ulid`,`amount`,`date`)VALUES('"+lid+"','"+amount+"',curdate())"
        payid=dd.insert(qq)

        qry="INSERT INTO `delivery_model`(`pid`,`name`,`phone`,`place`,`post`,`pincode`,`nearplace`)VALUES('"+pid+"','"+name+"','"+phone+"','"+place+"','"+post+"','"+pincode+"','"+nearplace+"')"
        dd.insert(qry)

        q="INSERT INTO `master_model`(`seller_id`,`user_id`,`product_id`,`payment_id`,`master_amount`,`date`)VALUES('"+sellerid+"','"+lid+"','"+pid+"','"+str(payid)+"','"+amount+"',curdate())"
        dd.insert(q)

        bankqry = "UPDATE bank SET amount=amount-'" + amount + "' WHERE bank='" + bank + "' AND `accpin`='" + pin + "'"
        dd.update(bankqry)

        q="UPDATE `product_model` SET `product_count`=`product_count`-1 WHERE `product_id`='"+pid+"'"
        dd.update(q)

        return jsonify(status="ok")
    else:
        return jsonify(status="low")

@app.route('/user_view_purchase_history',methods=["post"])
def user_view_purchase_history():
    lid=request.form["lid"]
    q="SELECT `seller_model`.*,`product_model`.*,`master_model`.* FROM `master_model` INNER JOIN `product_model` ON `master_model`.`product_id`=`product_model`.`product_id` INNER JOIN `seller_model` ON `product_model`.`seller_id`=`seller_model`.`login_id` WHERE `master_model`.`user_id`='"+lid+"'"
    d=Db()
    print(q)
    res=d.select(q)
    print(res)
    return jsonify(status="ok",data=res)

@app.route('/user_send_rating',methods=["post"])
def user_send_rating():
    lid=request.form["ulid"]
    slid=request.form["pid"]
    rating=request.form["rating"]

    q="INSERT INTO `rating_model`(`ulid`,`pid`,`r_date`,`rating`)VALUES('"+lid+"','"+slid+"',CURDATE(),'"+rating+"')"
    d=Db()
    d.insert(q)
    return jsonify(status="ok")
@app.route("/and_user_view_tutorial",methods=['post'])
def and_user_view_tutorial():
    db=Db()
    qry="SELECT `tutorial_model`.*, `seller_model`.* FROM `seller_model` INNER JOIN `tutorial_model` ON `tutorial_model`.`seller_id`=`seller_model`.`login_id`"
    res=db.select(qry)

    return jsonify(status='ok',data=res)

@app.route('/user_view_all_products',methods=["post"])
def user_view_all_products():
    q="SELECT `seller_model`.*,`product_model`.* FROM `seller_model` INNER JOIN `product_model` ON `seller_model`.`login_id`=`product_model`.`seller_id` where product_count>0"
    d=Db()
    res=d.select(q)
    return jsonify(status="ok",data=res)

@app.route('/user_view_all_products_search',methods=["post"])
def user_view_all_products_search():
    name=request.form["name"]
    q="SELECT `seller_model`.*,`product_model`.* FROM `seller_model` INNER JOIN `product_model` ON `seller_model`.`login_id`=`product_model`.`seller_id` where (`product_model`.`product_name` like '%"+name+"%' or `product_model`.`product_details` like '%"+name+"%') and product_count>0"
    d=Db()
    res=d.select(q)
    return jsonify(status="ok",data=res)
@app.route('/user_subscription',methods=["post"])
def user_subscription():
    lid=request.form["lid"]
    q="SELECT * FROM user_model WHERE `login_id`='"+lid+"'"
    d=Db()
    res2=d.selectOne(q)
    print(res2)
    if res2 is not None:
        q3="SELECT DATEDIFF(CURDATE(),'"+res2["reg_date"]+"') as dayys"
        res=d.selectOne(q3)
        print("----", res, type(res))
        if res["dayys"] is not None:
            if int(res["dayys"])>2:
                q="SELECT `package_model`.*,`buy_model`.* FROM `buy_model` INNER JOIN `package_model` ON `package_model`.`package_id`=`buy_model`.`package_id` WHERE `buy_model`.`user_lid`='"+lid+"' and buy_model.status='active' "
                d=Db()
                re=d.selectOne(q)

                print("________________________package--",re)
                if re is not None:
                    cc=Db()
                    q4 = "SELECT DATEDIFF(CURDATE(),'" + re["buy_date"] + "') as dayys"
                    print("********************",q4)
                    re1=cc.selectOne(q4)
                    print("----**", re1, type(re1))
                    if re1["dayys"] > int(re["p_details"]):
                        print("--exeed")
                        uppack="UPDATE `buy_model` SET `status`='deactive' WHERE `buy_id`='"+str(re["buy_id"])+"'"
                        cp=Db()
                        cp.update(uppack)


                        return jsonify(status="ok", day="exeed")

                    elif  re1["dayys"] < int(re["p_details"]):
                        return jsonify(status="ok", day="noexeed")
                    else:return jsonify(status="ok", day="exeed")

                return jsonify(status="ok", day="exeed")
            else:
                return jsonify(status="ok", day="noexeed")
        else:
            return jsonify(status="ok", day="noexeed")

    else:
        return jsonify(status="no")




if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5050)


