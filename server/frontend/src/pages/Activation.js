import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from "react-router-dom";
import authApi from '../api/authApi';
import EmailForm from '../components/EmailForm';

export function Activation() {
    const { uid, token } = useParams();
    const navigate = useNavigate();
    const [Success, setSuccess] = useState(false);

    useEffect(() => {
        if (uid && token) {
            authApi.Activate(uid, token)
                .then(data => {
                    console.log('成功しました', data);
                    setSuccess(true);
                })
                .catch(error => {
                    console.log('失敗しました', error);
                });
        }
    }, [uid, token]);

    if (Success) {
        return (
            <div>
                <h1>本登録完了</h1>
            </div>
        )
    } else {
        return (
            <div>
                <h1>本登録失敗</h1>
                <button onClick={() => navigate('/resendactivation')}>再度メールを送信</button>
            </div>
        )
    }

}

export function ResendActivation() {
    const navigate = useNavigate();
    const [errorMessage, setError] = useState("");

    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        if (!data.get("email")) {
            setError("メールアドレスを入力してください。");
            return;
        }
        authApi.ResendActivation(data)
            .then((res) => {
                console.log('成功しました', res);
                navigate("/");
                setError("");
            })
            .catch((error) => {
                console.log('エラー:', error)
                if (error.response?.status === 400) {
                    setError("認証待ちメールアドレスに該当しませんでした。");
                    return;
                }
                const message = "Something went wrong.";
                setError(message);
            });
    };

    return (
        <EmailForm handleSubmit={handleSubmit} errorMessage={errorMessage} />
    )
}
