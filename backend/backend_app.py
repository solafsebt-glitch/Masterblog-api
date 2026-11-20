from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def generate_next_id(posts):
    """Generate the next unique integer ID based on existing posts."""
    if not posts:
        return 1
    return max(post["id"] for post in posts) + 1


def validate_post_payload(data):
    """Validate incoming JSON payload and return missing required fields."""
    if not isinstance(data, dict):
        return ["title", "content"]

    missing_fields = []
    for field in ("title", "content"):
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            missing_fields.append(field)
    return missing_fields


def find_post_by_id(post_id):
    """Find and return a post dictionary by its integer ID, or None if not found."""
    for post in POSTS:
        if post["id"] == post_id:
            return post
    return None


@app.route("/api/posts", methods=["GET"])
def get_posts():
    """Return all blog posts as a JSON list."""
    return jsonify(POSTS), 200


@app.route("/api/posts", methods=["POST"])
def add_post():
    """Create a new blog post from JSON input and return it with status 201."""
    data = request.get_json(silent=True)
    missing_fields = validate_post_payload(data)

    if missing_fields:
        return (
            jsonify(
                {
                    "error": "Missing required fields",
                    "missing_fields": missing_fields,
                }
            ),
            400,
        )

    new_post = {
        "id": generate_next_id(POSTS),
        "title": data["title"].strip(),
        "content": data["content"].strip(),
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    """Delete an existing blog post by ID and return a confirmation message."""
    post = find_post_by_id(post_id)

    if post is None:
        return jsonify({"error": f"Post with id {post_id} was not found."}), 404

    POSTS.remove(post)
    return (
        jsonify(
            {"message": f"Post with id {post_id} has been deleted successfully."}
        ),
        200,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)