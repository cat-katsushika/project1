import * as React from "react";
import { Outlet } from 'react-router-dom';
import Header from "../Header";

const LoginButtonObject = { title: "LOG IN", url: "/login" };
const ResetPasswordObject = { title: "Reset Password", url: "/reset_password_email_form"};
const ResetUsernameObject = { title: "Reset Username", url: "/reset_username_email_form"};
const UserObject = { title: "User Profile", url: "/user" };
const sectionList = [LoginButtonObject, ResetPasswordObject, ResetUsernameObject, UserObject];

export default function DefaultLayout(){
  return (
    <>
      <Header title="TwtterClone-C" sections={sectionList} />
      <Outlet />
    </>
  );
};
