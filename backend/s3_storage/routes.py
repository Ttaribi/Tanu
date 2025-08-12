from . import s3_storage_bp
from backend.clients import s3_client, S3_BUCKET
from flask import request, jsonify, render_template
from uuid6 import uuid7

@s3_storage_bp.route("/upload")
def upload_page():
    return render_template("storage.html")

@s3_storage_bp.route("/gen-presigned", methods=["POST"])
def gen_sign():
    data = request.json
    post_id = uuid7()
    key = f"public/posts/{post_id}"
    url = s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket":S3_BUCKET,
            "Key":key,
            "ContentType": data['content_type']
        },
        ExpiresIn=30
    )
    return jsonify({'post_id': post_id, "url": url, "key": key})