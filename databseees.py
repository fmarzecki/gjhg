from app import db, Users , Trainers
readers = Users.query.get(3)
print(readers.username)


user = Users.query.filter_by(username='heh').first()
print(user.email)

trainer = Trainers.query.get(1)
print(trainer.trainer_name)


user = Users.query.get(3)
user_3_trainer_name = user.trainers.all()

for i in user_3_trainer_name:
    print(i.trainer_name)

