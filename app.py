from flask import render_template, redirect, flash, session, jsonify, Flask, request
import send_email
from auth import login, email_verified, fetch_userid
import like
from comment import *
import share
import conn
import post_content, follow, report
import admin, user

from uprofile import profile_select, user_select, profile_update, user_update, user_update_admin, profile_create, profile_photo

from admin import admin_create, admin_check, admin_name, admin_delete, admin_select, admin_updates, admins_all, admins_self_update
from user import users_all, user_one, user_create, fetchall_user

from admin_post import  ad_image_one, ad_update_status,  ad_video_one, ad_album_one, ad_share_one
from upwd import check_pwd, change_pwd, reset_pwd


mycursor = conn.mydb.cursor(buffered=True)
app = Flask(__name__)
app.secret_key = 'onlyiknow'


""" Authenticate user login  """
@app.route('/', methods=['GET', 'POST'])
def mainpage():
    if 'userid' in session:
        return redirect('/homepage')
    elif 'userid' not in session:
        log = login()
        if log == 'Success':
            return redirect('/homepage')
        else:
            return render_template("loginpage.html")


""" User signup """
@app.route('/signup', methods=['GET', 'POST'])
def signup_request():
    if request.method == "POST":
        username = request.form.get('uname')
        pwd = request.form.get('pwd')
        cpwd = request.form.get('cpwd')
        name = request.form.get("name")
        users = fetchall_user()
        for check in users:
            if check[1] == username:
                flash("Username already exist, please choose another")
                return redirect('/signup')
        if pwd != cpwd:
            flash("Confirm password does not same")
            return redirect('/signup')
        elif pwd == cpwd:
            email = request.form.get('email')
            user_id = user_create(username, pwd, email)
            send_email.email(email, user_id, name)
            return render_template('registration/registration_success.html')
    return render_template('registration/signup.html')


""" Send User Password reset email """
@app.route('/username', methods=["POST"])
def username_check():
    username = request.form.get("username")
    user = fetch_userid(username)
    send_email.change_pwd_email(user[1], user[0])
    return redirect('/')


""" User Password reset """
@app.route('/pwdreset/<uid>')
def pwd_reset(uid):
    reset_pwd(uid)
    return redirect('/')


""" User Account Verified """
@app.route('/emailverified/<uid>/<name>')
def email_verify(uid, name):
    email_verified(uid)
    profile_create(uid, name)
    return redirect('/')


""" Homepage """
@app.route('/homepage')
def homepage():
    if 'userid' in session:
        userid = session['userid']
        upro = profile_select(userid)
        myresult = post_content.Post_content.fetchall_user(userid)
        relatenum = follow.Follow.relationship_num(userid)
        following = follow.Follow.fetchall_following(userid)
        follower = follow.Follow.fetchall_follower(userid)
        shares = share.fetchall_user(userid)
        return render_template('homepage.html', userid=userid, myresult=myresult, shares=shares,
                               upro=upro, relatenum=relatenum, followings=following, followers=follower)
    else:
        return redirect('/')


""" User profile """
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'userid' in session:
        userid = session['userid']
        user = user_select(userid)
        upro = profile_select(userid)
        if request.method == "POST":
            name = request.form.get('upname')
            gender = request.form.get('gender')
            status = request.form.get('status')
            dob = request.form.get('dob')
            email = request.form.get('email')
            profile_update(userid, name, gender, status, dob)
            user_update(userid, email)
            return redirect('/homepage')
        else:
            return render_template('profile.html', upro=upro, user=user, userid=userid)
    else:
        return redirect('/')


""" User password """
@app.route('/profile/password', methods=['GET', 'POST'])
def profile_pwd():
    if 'userid' in session:
        if request.method == "POST":
            oldpwd = request.form.get('oldpwd')
            if oldpwd == check_pwd(session['userid']):
                newpwd = request.form.get('newpwd')
                cpwd = request.form.get('cpwd')
                if newpwd == cpwd:
                    change_pwd(cpwd, session['userid'])
                    return redirect('/profile/password')
                else:
                    flash("New and confirm password does not match")
                    return redirect('/profile/password')
            else:
                flash("Old password does not correct")
                return redirect('/profile/password')
        else:
            return render_template('profile/change_pwd.html', userid=session['userid'])
    else:
        return redirect('/')


""" User profile photo """
@app.route('/profile/picture', methods=['GET', 'POST'])
def profile_pic():
    if 'userid' in session:
        if request.method == "POST":
            profile_photo(session['userid'])
            return redirect('/profile/picture')
        else:
            pic = profile_select(session['userid'])
            return render_template('profile/profile_picture.html', pic=pic[6], userid=session['userid'])
    else:
        return redirect('/')


""" Userpage """
@app.route('/userpage')
def userpage():
    if 'userid' in session:
        userid = session['userid']
        myresult = post_content.Post_content.fetchall_other(userid)
        """random.shuffle(myresult)"""
        suggest = follow.Follow.suggestion(userid)
        following = follow.Follow.fetchall_following(userid)
        return render_template('userpage.html', userid=userid, myresult=myresult, name=session['name'],
                               followers=suggest, followings=following)
    else:
        return redirect('/')

@app.route('/suggest')
def suggestion():
    if 'userid' in session:
        userid = session['userid']
        suggest = follow.Follow.suggestion(userid)
        return render_template('suggest.html', userid=userid, name=session['name'], suggests=suggest)
    else:
        return redirect('/')

""" User Delete post  """
@app.route('/post_update/<cid>', methods=['POST'])
def post_deactive(cid):
    sql = "Update post_content set Post_status='Deleted' where CID='" + cid + "'"
    try:
        mycursor.execute(sql)
        mydb.commit()
    except:
        conn.mydb.ping(True)
        mycursor.execute(sql)
        mydb.commit()
    return redirect('/homepage')


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if 'adminid' not in session:
        if request.method == "POST":
            uname = request.form.get('uname')
            pwd = request.form.get('pwd')
            admin = admin_check(uname, pwd)
            for check in admin:
                if check[1] == uname and check[2] == pwd:
                    session['adminid'] = check[0]
                    return redirect('/dashboard')
                elif check[1] != uname or check[2] != pwd:
                    flash('Password or username are wrong')
                    return redirect('/admin')
        return render_template('admin/Adminlogin.html')
    else:
        return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'adminid' in session:
        aid = admin_name(session['adminid'])
        reports = report.Report.fetchall(session['adminid'])
        return render_template('admin/dashboard.html', admin=aid, aid=session['adminid'], db=reports)
    else:
        return redirect('/admin')

@app.route('/admin_user')
def user_all():
    if 'adminid' in session:
        aid = admin_name(session['adminid'])
        users = users_all()
        return render_template('admin/admin_user.html', users=users, admin=aid, aid=session['adminid'])
    else:
        return redirect('/admin')


@app.route('/admin_view_profile/<uid>', methods=['GET'])
def user_info(uid):
    if 'adminid' in session:
        admin = admin_name(session['adminid'])
        user = user_one(uid)
        upro = profile_select(uid)
        return render_template('admin/admin_view_profile.html', user=user, upro=upro, admin=admin, aid=session['adminid'])
    else:
        return redirect('/admin')

@app.route('/user_delete/<uid>')
def user_deletes(uid):
    user.user_delete(uid)
    return redirect('/admin_user')

@app.route('/admin_view', methods=['GET'])
def admin_all():
    if 'adminid' in session:
        aid = admin_name(session['adminid'])
        admins = admins_all(session['adminid'])
        return render_template('admin/admin_view.html', admins=admins, admin=aid, aid=session['adminid'])

@app.route('/admin_delete/<uid>', methods=['GET'])
def admin_delete(uid):
    sql = "Delete from admin where AdminID='" + uid + "'"
    mycursor.execute(sql)
    mydb.commit()
    return redirect('/admin_view')

@app.route('/admin_create', methods=['POST', 'GET'])
def admin_create():
    aid = admin_name(session['adminid'])
    if request.method == "POST":
        uname = request.form.get('uname')
        pwd = request.form.get('pwd')
        rpwd = request.form.get('rpwd')
        if rpwd == pwd:
            admin_create(uname, rpwd)
            return redirect('/admin_view')
        elif rpwd != pwd:
            flash("Password wrong")
            return redirect('/admin_create')
        else:
            return redirect('/admin_create')
    else:
        return render_template('admin/AdminCreate.html', admin=aid, aid=session['adminid'])

@app.route('/admin_update/<aid>', methods=['POST'])
def admin_update(aid):
    if 'adminid' in session:
        if request.method == "POST":
            admin_updates('adminsnss', aid)
            return redirect('/admin_view')
    else:
        return redirect('/admin')

@app.route('/admin_delete/<aid>')
def admin_deletes(aid):
    if 'adminid' in session:
        admin.admin_delete(aid)
        return redirect('/admin_view')
    else:
        return redirect('/admin')

@app.route('/admin_self_update/<aid>', methods=['GET', 'POST'])
def admin_self_update(aid):
    if 'adminid' in session:
        admin = admin_name(session['adminid'])
        if request.method == "POST":
            name = request.form.get('name')
            oldpwd = request.form.get('opwd')
            newpwd = request.form.get('npwd')
            cpwd = request.form.get('cpwd')
            ad = admin_select(aid)
            if oldpwd == "" or newpwd == "" or cpwd == "":
                admins_self_update(name, aid)
                return redirect('/dashboard')
            elif oldpwd == ad[3] and newpwd == cpwd:
                admin_updates(cpwd, aid)
                return redirect('/admin_view')
            elif oldpwd != ad[3] or newpwd != cpwd:
                flash("Password wrong")
                return redirect('/admin_self_update/' + aid)
        else:
            ad = admin_select(aid)
            return render_template('admin/admin_self.html', ad=ad, admin=admin, aid=aid)
    else:
        return redirect('/admin')

@app.route('/postdb', methods=['GET'])
def postdb():
    if 'adminid' in session:
        admin = admin_name(session['adminid'])
        type = request.args.get("type")
        postdb = post_content.Post_content("", "").fetchall(type)
        url = ""
        if type == "Photo":
            url = 'admin/photo/image_all.html'
        elif type == "Video":
            url = 'admin/video/video_all.html'
        elif type == "Album":
            url = 'admin/album/album_all.html'
        elif type == "Share":
            postdb = share.fetchall_share()
            url = 'admin/share/share_all.html'
        return render_template(url, admin=admin, aid=session['adminid'], db=postdb)
    else:
        return redirect('/admin')

@app.route('/admin_share_view/<sid>/<types>', methods=['GET'])
def admin_share_view(sid, types):
    if 'adminid' in session:
        global post
        admin = admin_name(session['adminid'])
        shares = ad_share_one(sid)
        if types == "Photo":
            post = ad_image_one(shares[1])
        elif types == "Video":
            post = ad_video_one(shares[1])
        reaction = post_content.Post_content.post_num(sid, '')
        return render_template('admin/share/share_one.html', admin=admin, aid=session['adminid'],
                               post=post, share=shares, react=reaction)
    else:
        return redirect('/admin')

@app.route('/admin_album_view/<cid>', methods=['GET'])
def admin_album_view(cid):
    if 'adminid' in session:
        admin = admin_name(session['adminid'])
        app = ad_album_one(cid)
        reaction = post_content.Post_content.post_num(cid, '')
        return render_template('admin/album/album_one.html', admin=admin, aid=session['adminid'],
                               app=app, react=reaction)
    else:
        return redirect('/admin')

@app.route('/admin_photo_view/<cid>', methods=['GET'])
def admin_photo_view(cid):
    if 'adminid' in session:
        admin = admin_name(session['adminid'])
        app = ad_image_one(cid)
        reaction = post_content.Post_content.post_num(cid, '')
        return render_template('admin/photo/image_one.html', admin=admin, aid=session['adminid'],
                               app=app, react=reaction)
    else:
        return redirect('/admin')

@app.route('/admin_video_view/<cid>', methods=['GET'])
def admin_video_view(cid):
    if 'adminid' in session:
        admin = admin_name(session['adminid'])
        avp = ad_video_one(cid)
        reaction = post_content.Post_content.post_num(cid, '')
        return render_template('admin/video/video_one.html', admin=admin, aid=session['adminid'],
                               app=avp, react=reaction)
    else:
        return redirect('/admin')

@app.route('/admin_photo_update/<cid>', methods=['GET'])
def admin_photo_update(cid):
    if 'adminid' in session:
        admin = admin_name(session['adminid'])
        app = ad_image_one(cid)
        return render_template('admin/photo/image_update.html', admin=admin, aid=session['adminid'], app=app)
    else:
        return redirect('/admin')


@app.route('/admin_album_update/<cid>', methods=['GET'])
def admin_album_update(cid):
    if 'adminid' in session:
        admin = admin_name(session['adminid'])
        app = ad_album_one(cid)
        return render_template('admin/album/album_update.html', admin=admin, aid=session['adminid'], app=app)
    else:
        return redirect('/admin')


@app.route('/admin_video_update/<cid>', methods=['GET'])
def admin_video_update(cid):
    if 'adminid' in session:
        admin = admin_name(session['adminid'])
        app = ad_video_one(cid)
        return render_template('admin/video/video_update.html', admin=admin, aid=session['adminid'], app=app)
    else:
        return redirect('/admin')

@app.route('/admin_share_update/<sid>/<types>', methods=['GET', 'POST'])
def admin_share_update(sid, types):
    if 'adminid' in session:
        if request.method == "POST":
            status = request.form.get('status')
            share.update_status(sid, status)
            url = "/admin_share_update/{}/{}".format(sid, types)
            return redirect(url)
        else:
            global post
            admin = admin_name(session['adminid'])
            shares = ad_share_one(sid)
            if types == "Photo":
                post = ad_image_one(shares[1])
            elif types == "Video":
                post = ad_video_one(shares[1])
            return render_template('admin/share/share_update.html', admin=admin, aid=session['adminid'],
                                   post=post, share=shares)
    else:
        return redirect('/admin')

@app.route('/admin_react/<react>')
def admin_react(react):
    if 'adminid' in session:
        global template, reacts
        admin = admin_name(session['adminid'])
        if react == "like":
            reacts = like.fetchall()
            template = 'admin/react/like_all.html'
        elif react == "comment":
            reacts = fetchall()
            template = 'admin/react/comment_all.html'
        return render_template(template, admin=admin, aid=session['adminid'], reacts=reacts)
    else:
        return redirect('/admin')

@app.route("/admin_comment/<id>", methods=["GET"])
def admin_comment(id):
    if 'adminid' in session:
        global post
        admin = admin_name(session['adminid'])
        comment = fetchone(id)
        types = post_content.Post_content.fetchone(comment[2])
        if types[1] == "Photo":
            post = ad_image_one(types[0])
        elif types[1] == "Video":
            post = ad_video_one(types[0])
        elif types[1] == "Album":
            post = ad_album_one(types[0])
        return render_template('admin/react/comment_one.html', admin=admin,
                               aid=session['adminid'], comment=comment, post=post, types=types[1])
    else:
        return redirect('/admin')

@app.route('/admin_post_delete/<cid>', methods=['DELETE'])
def admin_post_delete(cid):
    if 'adminid' in session:
        post_content.Post_content.delete(cid)
        return 'Delete Success'
    else:
        return redirect('/admin')

@app.route('/admin_post_update/<cid>', methods=['POST'])
def admin_post_update(cid):
    if 'adminid' in session:
        type = request.args.get("type").lower()
        if request.method == "POST":
            status = request.form.get('status')
            ad_update_status(status, cid)
            url = "/admin_{}_update/{}".format(type, cid)
            return redirect(url)
        else:
            return redirect('/admin')
    else:
        return redirect('/admin')


@app.route('/admin_relationship', methods=["GET"])
def admin_relationship():
    if 'adminid' in session:
        admin = admin_name(session['adminid'])
        relatedb = follow.Follow.fetchall("")
        return render_template('admin/relation/relation_all.html', admin=admin, aid=session['adminid'], db=relatedb)
    else:
        return redirect('/admin')

@app.route('/admin_relation_view/<uid>', methods=["GET"])
def admin_relationship_view(uid):
    if 'adminid' in session:
        rnum = follow.Follow.relationship_num(uid)
        relate = follow.Follow.fetchall_user(uid)
        return render_template('admin/relation/relation_one.html', admin=admin, aid=session['adminid'],
                               rnum=rnum, relate=relate, uid=uid)
    else:
        return redirect('/admin')

@app.route('/admin_relation_delete/<id>')
def admin_relationship_delete(id):
    if 'adminid' in session:
        follow.Follow.delete(id)
        return redirect('/admin_relationship')
    else:
        return redirect('/admin')

@app.route('/reportdb', methods=["GET"])
def reportdb():
    if 'adminid' in session:
        admin = admin_name(session['adminid'])
        reportdb = report.Report_info.fetchall('')
        return render_template('admin/report/report_all.html', admin=admin, aid=session['adminid'], db=reportdb)
    else:
        return redirect('/admin')

@app.route('/admin_handle/<reportid>')
def admin_handle(reportid):
    if 'adminid' in session:
        report.Report(reportid, session['adminid']).handle()
        return redirect('/reportdb')
    else:
        return redirect('/admin')

@app.route('/admin_remove/<rid>')
def admin_remove(rid):
    if 'adminid' in session:
        report.Report.remove(rid)
        return redirect('/dashboard')
    else:
        return redirect('/admin')

@app.route('/admin_completed/<rid>', methods=["POST"])
def admin_complete(rid):
    if 'adminid' in session:
        report.Report.completed(rid)
        return redirect('/dashboard')
    else:
        return redirect('/admin')

@app.route('/admin_repinfo/<rid>')
def admin_repinfo(rid):
    if 'adminid' in session:
        global post
        admin = admin_name(session['adminid'])
        reports = report.Report.fetchone(rid)
        repinfo = report.Report_info.fetchone(reports[1])
        types = post_content.Post_content.fetchone(repinfo[1])
        if types[1] == "Photo":
            post = ad_image_one(types[0])
        elif types[1] == "Video":
            post = ad_video_one(types[0])
        elif types[1] == "Album":
            post = ad_album_one(types[0])
        return render_template('/admin/report/repinfo_one.html', admin=admin, aid=session['adminid'],
                               report=reports, rinfo=repinfo, post=post)
    else:
        return redirect('/admin')

@app.route('/logout_admin')
def logout_admin():
    if 'adminid' in session:
        session.pop('adminid', None)
        return redirect('/admin')
    else:
        return redirect('/admin')

@app.route('/logout')
def logout():
    if 'userid' in session:
        session.pop('userid', None)
        return redirect('/')
    else:
        return redirect('/')

@app.route('/post/<pid>', methods=['GET', 'POST'])
def post(pid):
    if 'userid' in session:
        global myresult
        global template
        userid = session['userid']
        comment = comment_list(pid)
        if pid[0] == "C":
            myresult = post_content.Post_content.fetchpost(pid, userid)
            if request.args.get("id") == userid:
                template = "user_post.html"
            else:
                template = "post.html"
        elif pid[0] == "S":
            myresult = share.fetchone(pid, userid)
            if request.args.get("id") == userid:
                template = "share/share_user_post.html"
            else:
                template = "share/share_post.html"
        return render_template(template, userid=userid, myresult=myresult, comments=comment)
    else:
        return redirect('/')


@app.route('/data', methods=["POST", "GET"])
def data():
    search = request.form.get("text")
    sql = "Select Name, UserID from userprofile where Name LIKE '%{}%'".format(search)
    try:
        mycursor.execute(sql)
        result = mycursor.fetchall()
    except:
        conn.mydb.ping(True)
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        mycursor.execute(sql)
        result = mycursor.fetchall()
    return jsonify(result)


@app.route('/like_request/<user_id>/<cid>', methods=["POST", "DELETE"])
def like_request(user_id, cid):
    like.request_like(user_id, cid)
    return 'Success'

@app.route('/comment_request/<user_id>/<cid>', methods=["POST", "DELETE", "PATCH"])
def comment_request(user_id, cid):
    ucomment = request.form.get("comment")
    commentID = request.args.get("comment_id")
    comment(ucomment, user_id, cid)
    comment_edit(commentID, ucomment)
    delete_comment(commentID, user_id)
    return 'Success'

@app.route('/share_request/<uid>', methods=["POST", "DELETE", "PATCH"])
def share_request(uid):
    postID = request.args.get("postID")
    if request.method == "POST":
        text = request.args.get("text")
        share.share(postID, text, uid)
        return 'Share Success'
    elif request.method == "PATCH":
        text = request.args.get("text")
        share.update(postID, text)
        return 'Update Success'

@app.route('/share_status', methods=["PATCH"])
def share_status():
    postID = request.args.get("postID")
    if request.method == "PATCH":
        status = request.args.get("status")
        share.update_status(postID, status)
        return 'Delete Success'


@app.route('/create_post', methods=["POST", "GET"])
def create_post():
    if 'userid' in session:
        if request.method == "POST":
            text = request.form.get('description')
            post_content.Post_content(text, session['userid']).method_request()
            return redirect('/homepage')
        return render_template('create.html', userid=session['userid'])
    else:
        return redirect('/')

@app.route('/update_post', methods=["POST", "GET"])
def update_post():
    if 'userid' in session:
        if request.method == "POST":
            files = request.files.getlist("files")
            text = request.form.get("description")
            cid = request.args.get("cid")
            file_type = ""
            if len(files) > 1:
                file_type = "Album"
            elif len(files) == 1:
                file_type = files[0].filename.split(".")[-1]
                if file_type in ['gif', 'png', 'jpg', 'jpeg']:
                    file_type = "Photo"
                elif file_type in ['mp4', 'mov', 'avi', 'webm']:
                    file_type = "Video"
                else:
                    file_type = request.args.get("type")
            post_content.Post_content(text, session['userid']).update(file_type, cid, files)
            return redirect('/post/{}?id={}&type={}'.format(cid, session['userid'], file_type))
        else:
            cid = request.args.get("cid")
            myresult = post_content.Post_content.fetchpost(cid, session['userid'])
            return render_template('update.html', userid=session['userid'], myresult=myresult)
    else:
        return redirect('/')


@app.route('/post_delete', methods=["DELETE"])
def post_delete():
    cid = request.args.get("cid")
    status = request.args.get('status')
    ad_update_status(status, cid)
    return 'Delete Success'


@app.route('/<userid>', methods=["GET"])
def userprofile(userid):
    if 'userid' in session:
        if userid == session['userid']:
            return redirect('/')
        elif userid != session['userid']:
            upro = profile_select(userid)
            relatenum = follow.Follow.relationship_num(userid)
            follower = follow.Follow.fetchall_follower(session['userid'])
            myresult = post_content.Post_content.fetchall_user(userid)
            shares = share.fetchall_user(userid)
            return render_template('Profile/user_profile.html', userid=session['userid'], myresult=myresult, upro=upro,
                                   shares=shares, relatenum=relatenum, followers=follower)
    else:
        return redirect('/')


@app.route('/report', methods=["POST"])
def reports():
    id = request.form.get("id")
    description = request.form.get("report")
    rid = report.Report_info(id, description, session['userid']).method_request()
    report.Report(rid, "").method_request()
    return 'Report success'


@app.route('/unfollow', methods=["DELETE"])
def unfollows():
    relateID = request.args.get("relateId")
    follow.Follow.method_request(relateID)
    return 'Unfollow success'

@app.route('/relatelist', methods=["GET"])
def relatelist():
    cid = request.args.get("cid")
    react = request.args.get("react")
    sql = "SELECT DISTINCT up.Profile_pic, up.Name, t.UserID, r.UserID_2 FROM `{}` as t \
              left join userprofile as up on up.UserID = t.UserID \
              left join relationship as r on r.UserID_2 = t.UserID \
              WHERE t.CID='{}'".format(react, cid)
    try:
        mycursor.execute(sql)
        result = mycursor.fetchall()
    except:
        conn.mydb.ping(True)
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        mycursor.execute(sql)
        result = mycursor.fetchall()
    return jsonify(result)


@app.route('/relationship', methods=["POST", "DELETE", "PATCH"])
def relations():
    user = request.args.get("userid")
    if request.method == "POST":
        follow.Follow(session['userid'], user).method_request()
    elif request.method == "DELETE":
        relateID = request.args.get("relateId")
        follow.Follow.method_request(relateID)
    elif request.method == "PATCH":
        follow.Follow(session['userid'], user).block()
    return 'success'

@app.template_filter()
def split(string):
    return string.split()

@app.template_filter()
def userpic(uid):
    return profile_select(uid)[6]

@app.template_filter()
def user_relationship(uid1, uid2):
    return follow.check_relation(uid1, uid2)

@app.template_filter()
def post_status(pid):
    return post_content.Post_content.status(pid)


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True, threaded=True)





