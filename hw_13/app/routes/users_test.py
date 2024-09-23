# Binary Avatarts, stored in db
# @router.patch('/avatar', response_model=UserResponse)
# async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
#                              db: Session = Depends(get_db)):
#     if file.content_type not in ["image/jpeg", "image/png"]:
#         raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG and PNG are supported.")
#
#         # Read the uploaded file's binary data
#     avatar_data = await file.read()
#     #print(avatar_data)
#     current_user.avatarBinary = avatar_data
#     db.add(current_user)
#     db.commit()
#     db.refresh(current_user)
#     return current_user
#
#
# @router.get('{user_id}/avatar', response_class=StreamingResponse)
# async def get_user_avatar(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user or not user.avatarBinary:
#         raise HTTPException(status_code=404, detail="User or avatar not found")
#
#     return Response(content=user.avatarBinary, media_type="image/jpeg" if user.avatarBinary[:3] == b'\xff\xd8\xff' else "image/png")