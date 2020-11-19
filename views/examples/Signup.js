import React, { Component } from 'react';
import './main.css';

import axios from 'axios';

// reactstrap components
import {
    Button,
    Card,
    CardHeader,
    CardBody,
    CardFooter,
    Form,
    Input,
    InputGroupAddon,
    InputGroupText,
    InputGroup,
    Container,
    Col
  } from "reactstrap";

class Signup extends Component {

    _signup = async function() {

        const id = document.getElementsByName('signup_id')[0].value.trim();
        const password = document.getElementsByName('signup_password')[0].value.trim();
        const psw_check = document.getElementsByName('signup_pswCheck')[0].value.trim();
        const name = document.getElementsByName('signup_name')[0].value.trim();
        
        let sex_select = document.getElementsByName('signup_sex_select')[0].value;
        const sex = sex_select;
    
        let age_select = document.getElementsByName('signup_age_select')[0].value;
        const age = age_select;
    
        const height = document.getElementsByName('signup_height')[0].value.trim();
        const weight = document.getElementsByName('signup_weight')[0].value.trim();


    const data = { id : id, 
        password : password, 
        name : name,  
        sex : sex, 
        age : age,
        height : height,
        weight : weight };
    const add_user = await axios('http://www.naver.com/testQuery1', {
        method : 'POST',
        headers: new Headers(),
        data : data
    })

    if(!add_user) {
        return alert('이미 존재하는 아이디입니다.');

    } else {
        alert('회원가입이 완료되었습니다.');
        return window.location.href = '/';
        }
    }

    render() {
        return (
            <div className="page-header clear-filter" filter-color="blue">
                <div
                    className="page-header-image"
                    style={{
                    backgroundImage: "url(" + require("assets/img/bg11.jpg") + ")"
                    }}
                ></div>
            <div>
                <form id='signup_form'>
                <div>
                    <h3 id='signup_title'> 회원가입 </h3>
                </div>
                <div className='Signup'>
                    <div>
                    {/* 아이디 */}
                    <div>
                        <h5> 아이디 </h5>
                        <input type='text' maxLength='20' name='signup_id'/>
                    </div>

                    {/* 비밀번호 */}
                    <div>
                        <h5> 비밀번호 </h5>
                        <input type='password' maxLength='15' name='signup_password'/>
                    </div>

                    {/* 비밀번호 */}
                    <div>
                        <h5> 비밀번호 확인 </h5>
                        <input type='password' maxLength='15' name='signup_pswCheck'/>
                    </div>
                </div>

                <div id='signup_section'>
                    {/* 이름 */}
                    <div>
                        <h5> 이름 </h5>
                        <input type='text' maxLength='10' name='signup_name'/>
                    </div>

                    {/* 성별 */}
                    <div>
                        <h5> 성별 </h5>
                        <select name='signup_sex_select'>
                            <option value='여자'> 여자 </option>
                            <option value='남자'> 남자 </option>
                        </select>
                    </div>

                    {/* 연령대 */}
                    <div>
                        <h5> 연령대 </h5>
                        <select name='signup_age_select'>
                            <option value='10대'> 10대 </option>
                            <option value='20대'> 20대 </option>
                            <option value='30대'> 30대 </option>
                            <option value='40대'> 40대 </option>
                            <option value='50대'> 50대 </option>
                            <option value='60대'> 60대 </option>
                        </select>
                    </div>

                    {/* 신장 */}
                    <div>
                        <h5> 신장 </h5>
                        <input type='text' maxLength='10' name='signup_height'/>
                    </div>

                    {/* 몸무게 */}
                    <div>
                        <h5> 몸무게 </h5>
                        <input type='text' maxLength='10' name='signup_weight'/>
                    </div>
                </div>
            </div>

            <div>
                <input type='button' value='가입하기' name='sigunup_submit'/>
            </div>
            </form>
        </div>
    </div>
        );
    }
}

export default Signup;