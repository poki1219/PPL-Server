import re
from flask import jsonify

from ..model.user import User
from ..model.user import Interest
from ..model.user import Paper
from app import db

# 회원가입한 회원 정보를 user모델(즉, user테이블에 넣기)
def save_new_user(data):
    # 맞는 email 형식인지 먼저 체크
    try:
        if checkmail(data['email']):
            user = User.query.filter_by(email=data['email']).first()
            # db에 중복되는 email 주소 없음.
            if user == None:
                new_user = User(
                    email=data['email'],
                    password=data['password'],
                )
                response_object = {
                    'status': 'success',
                    'message': '회원가입 되었습니다.'
                }
                db.session.add(new_user)
                db.session.commit()
                interests = data['interests'];
                for interest in interests:
                    new_interest = Interest(name=interest, user_id=new_user.id)
                    db.session.add(new_interest);
                
                # new_paper = Paper(
                #     abstract="dummy text",
                #     author="me",
                #     category="공학_토목공학",
                #     link="https://www.google.com",
                #     title="capstone design",
                #     year=2019,
                #     user_id=12,
                # )
                db.session.add(new_paper)
                db.session.commit()
                # db.session.close()
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': '이미 가입된 email 주소입니다.',
                }
                db.session.close()
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': '입력한 email 주소는 맞는 형식이 아닙니다.'
            }
            db.session.close()
            return response_object, 402
    except Exception as e:
        response_object = {
            'status': 'error',
            'message': str(e)
        }
        return response_object, 500
    finally:
        db.session.close()

def save_changes(data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        response_object = {
            'status': 'error',
            'message': str(e)
        }
        return response_object, 500
    finally:
        db.session.close()

def get_user(email):
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            interests = [interest.to_dict() for interest in user.interests]
            papers = [paper.to_dict() for paper in user.papers]
            response_object = {
                'status': 'success',
                'message': '회원 조회에 성공했습니다.',
                'data': {
                    'id': user.id,
                    'email' : user.email,
                    'category' : interests,
                    'library' : papers,
                }
            }
            db.session.close()
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': '해당 회원이 없습니다.',
                'data': {},
            }
            db.session.close()
            return response_object, 401
    except Exception as e:
        response_object = {
            'status': 'error',
            'message': str(e)
        }
        return response_object, 500
    finally:
        db.session.close()

# email 형식 체크
def checkmail(email):
    p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    result = p.match(email) != None
    
    #True, False로 return
    return result