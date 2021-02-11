import models
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict

settings = Blueprint("settings", "settings")
    
@settings.route('/', methods=['POST'])
def create_new_setting():
    payload = request.get_json()
    setting = models.PersonSetting.create(**payload)
    setting_dict = model_to_dict(setting)
    return jsonify(data=setting_dict, status={"code": 201, "message":"Successfully created settings for the user!"})

@settings.route('/', methods=["GET"])
@login_required
def get_settings():
    
    try:
        setting = models.PersonSetting.get_by_id(1) \
                  .join_from(models.PersonSetting, models.Person) \
                  .where(models.Person.id == current_user.id)
        setting_dict = model_to_dict(setting)
        return jsonify(data=setting_dict, status={"code": 200, "message": "Successfully grabbed settings"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404,\
                                        "message": "Error getting the settings"})
        
        
@settings.route('/update', methods=["PUT"])
@login_required
def update_settings():
    
    try:
        setting = models.PersonSetting.get_by_id(1) \
                  .join_from(models.PersonSetting, models.Person) \
                  .where(models.Person.id == current_user.id)
        payload = request.get_json()
        query = models.PersonSetting.update(**payload) \
                .where(models.PersonSetting.id==setting.id)
        query.execute()
        updated_settings = model_to_dict(models.PersonSetting.get_by_id(1))
        return jsonify(data=updated_settings, status={"code": 200, "message": "Successfully updated the settings"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404,\
                                        "message": "Error getting the settings"})
