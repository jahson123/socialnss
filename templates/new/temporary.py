"""
<progress value="0" max="100" id="uploader">0%</progress>
<input type="file" value="upload" id="fileButton"/>
<script src="https://www.gstatic.com/firebasejs/8.2.2/firebase-app.js"></script>
<script>
  var firebaseConfig = {
    apiKey: "AIzaSyAci0y2q2vdPlWEscYy9yGBnoT5G6pRfvw",
    authDomain: "unique-perigee-299514.firebaseapp.com",
    databaseURL: "https://unique-perigee-299514-default-rtdb.firebaseio.com",
    projectId: "unique-perigee-299514",
    storageBucket: "unique-perigee-299514.appspot.com",
    messagingSenderId: "780859428666",
    appId: "1:780859428666:web:186013295f48ab39958a03",
    measurementId: "G-X85C75VPCY"
  };
  firebase.initializeApp(firebaseConfig);

  var uploader = document.getElementById('uploader')
  var fileButton = document.getElementById('fileButton')

  fileButton.addEventListener('change', function(e)
  {
    var file = e.target.files[0];
    var storageRef = firebase.storage().ref('example/' + file.name);
    var task = storageRef.put(file)
    task.on('state_changed',
        function progress(snapshot) {
            var percentage = snapshot.bytesTransferred / snapshot.totalBytes ) * 100
        },
        function error(err) {
        },
        function complete()
        );
   });
</script>



"""

"""
<style media="screen">
        body
        {
        display: flex;
        min-height: 100vh;
        width: 1800%;
        padding: 0;
        margin: 0;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        background-color: grey;
        }
        #uploader
        {
        -webkit-appearance: none;
        appearance: none;
        width: 50%;
        margin-bottom: 10px;
        }
    </style>
"""

"""
var btnUpload = $("#upload_file"),
		btnOuter = $(".button_outer");
	btnUpload.on("change", function(e){
		var ext = btnUpload.val().split('.').pop().toLowerCase();
		if($.inArray(ext, ['gif','png','jpg','jpeg']) == -1) {
			$(".error_msg").text("Not an Image...");
		} else {
			$(".error_msg").text("");
			btnOuter.addClass("file_uploading");
			setTimeout(function(){
				btnOuter.addClass("file_uploaded");
			},3000);
			var uploadedFile = URL.createObjectURL(e.target.files[0]);
			setTimeout(function(){
				$("#uploaded_view").append('<img src="'+uploadedFile+'" />').addClass("show");
			},3500);
		}
	});
	$(".file_remove").on("click", function(e){
		$("#uploaded_view").removeClass("show");
		$("#uploaded_view").find("img").remove();
		btnOuter.removeClass("file_uploading");
		btnOuter.removeClass("file_uploaded");
	});
"""

"""
@app.route('/image', methods=['GET', 'POST'])
def image():
    if 'userid' in session:
        if request.method == "POST":
            file = request.files.get('img')
            photo_name = file.filename
            text = request.form.get('description')
            # create post_content data
            post_id = post_content.Post_content(text, session['userid']).method_request()
            # create photo data
            photo_id = Photo(photo_name, file).method_request()
            # create post_photo data
            Post_photo(post_id, photo_id).method_request()
            return redirect('/homepage')
        else:
            return render_template('image.html')
    else:
        return redirect('/')

@app.route('/video', methods=['GET', 'POST'])
def video():
    if 'userid' in session:
        if request.method == "POST":
            file = request.files.get('video')
            video_name = file.filename
            text = request.form.get('description')
            vid = video_create(file, video_name)
            cid_generator = string.ascii_letters + string.digits
            cid = 'C_' + ''.join(random.choice(cid_generator) for i in range(6))

            sql = "Insert into post_content (CID, Post_type, UserID, Post_status) \
                  values (%s, %s, %s, %s)"
            val = (cid, 'Video', session['userid'], 'Active')
            mycursor.execute(sql, val)
            mydb.commit()
            post_video_create(text, cid, vid)
            # create post_content data
            post_id = post_content.Post_content(text, session['userid']).method_request()
            # create video data
            video_id = Video(video_name, file).method_request()
            # create post_video data
            Post_video(post_id, video_id).method_request()
            return redirect('/homepage')
        return render_template('create.html')
    else:
        return redirect('/')

"""