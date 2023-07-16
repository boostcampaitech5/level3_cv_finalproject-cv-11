import qs from "qs";

const fastapi = (operation, url, params, success_callback, failure_callback) => {
    let method = operation;
    let content_type = "application/json";
    let body = JSON.stringify(params);

    if (operation === "formdata") {
        method = "post";
        content_type = "multipart/form-data";
    }
    if (operation === "login" || operation === "signin") {
        method = "post";
        content_type = "application/x-www-form-urlencoded";
        body = qs.stringify(params);
    }

    let _url = "http://49.50.161.9:30008" + url;
    if (method === "get") {
        _url += "?" + new URLSearchParams(params);
    }

    let options = {
        method: method,
        headers: {
            "Content-Type": content_type,
        },
    };

    if (method !== "get" && operation !== 'formdata') {
        options["body"] = body;
    }

    if (operation === "formdata") {
        options["body"] = params;
    }

    fetch(_url, options)
        .then((response) => {
            if (response.status >= 200 && response.status < 300) {
                return response.json(); // 응답 데이터를 JSON으로 변환하여 반환
            } else {
                throw new Error("Request failed with status " + response.status);
            }
        })
        .then((json) => {
            if (success_callback) {
                success_callback(json);
            }
        })
        .catch((error) => {
            if (failure_callback) {
                failure_callback(error);
            } else {
                alert(error.message);
            }
        });
};

export default fastapi;