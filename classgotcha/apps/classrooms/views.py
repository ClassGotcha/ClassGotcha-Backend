# -*- coding: utf-8 -*-
import os, uuid, re, json, datetime
from django.core.files.base import File
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny  # , IsStaff
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.decorators import detail_route, list_route, api_view, permission_classes, parser_classes

from models import Account, Classroom, Semester, Major, Professor
from ..chat.models import Room

from serializers import ClassroomSerializer
from ..posts.serializers import MomentSerializer, Note, NoteSerializer
from ..tasks.serializers import Task, TaskSerializer
from ..accounts.serializers import BasicAccountSerializer, BasicClassroomSerializer


class ClassroomViewSet(viewsets.ViewSet):
	queryset = Classroom.objects.all()
	permission_classes = (IsAuthenticated,)

	'''Can pass a filename as optional variable'''

	def upload(self, request, file_name=None):
		upload = request.FILES.get('file', False)
		if not upload:
			return None
		name, extension = os.path.splitext(upload.name)

		if file_name:
			name = file_name
		name = name + '_' + uuid.uuid4().hex + extension
		with open(name, 'wb+') as temp_file:
			for chunk in upload.chunks():
				temp_file.write(chunk)
		new_file = File(file=open(name))  # there you go
		return new_file

	def retrieve(self, request, pk):
		classroom = get_object_or_404(self.queryset, pk=pk)
		serializer = ClassroomSerializer(classroom)
		return Response(serializer.data)

	def update(self, request, pk):
		classroom = get_object_or_404(self.queryset, pk=pk)
		for (key, value) in request.data.items():
			if key in ['description', 'syllabus']:
				setattr(classroom, key, value)
		serializer = ClassroomSerializer(classroom)
		return Response(serializer.data)

	@staticmethod
	def search(request):
		search_token = request.data.get('search', False)
		if not search_token:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		# only class code
		if search_token.isdigit():
			classrooms = Classroom.objects.filter(class_code=search_token)
			serializer = ClassroomSerializer(classrooms, many=True)
			return Response(serializer.data)
		# major + class number
		else:
			match = re.match(r"([a-z]+) *([0-9]+)", search_token, re.I)
			if match:
				items = match.groups()
				class_major = items[0].upper()
				class_number = items[1]
				major = Major.objects.get(major_short=class_major)
				classrooms = Classroom.objects.filter(major=major, class_number=class_number)
				serializer = BasicClassroomSerializer(classrooms, many=True)
				return Response(serializer.data)
			else:
				# TODO STEVE: need to consider more circumstances
				return Response({})

	def validate(self, request, pk):
		classroom = get_object_or_404(self.queryset, pk=pk)
		if request.user in classroom.students:
			return Response(status=status.HTTP_200_OK)
		else:
			return Response({'error': 'You are not in this classroom'}, status=status.HTTP_403_FORBIDDEN)

	@parser_classes((MultiPartParser, FormParser,))
	def syllabus(self, request, pk):
		classroom = get_object_or_404(self.queryset, pk=pk)
		new_file = self.upload(request, file_name=classroom.class_code)
		if not new_file:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		classroom.syllabus = new_file
		classroom.save()
		return Response(status=status.HTTP_200_OK)

	@parser_classes((MultiPartParser, FormParser,))
	def notes(self, request, pk):
		classroom = get_object_or_404(self.queryset, pk=pk)
		if request.method == 'POST':
			new_file = self.upload(request, file_name=classroom.class_code)
			if not new_file:
				return Response(status=status.HTTP_400_BAD_REQUEST)
			new_note = Note(file=new_file)
			new_note.creator = request.user
			new_note.classroom = classroom
			new_note.save()
			return Response(status=status.HTTP_201_CREATED)

		if request.method == 'GET':
			serializer = NoteSerializer(classroom.notes, many=True)
			return Response(serializer.data)

	def recent_moments(self, request, pk):
		classroom = get_object_or_404(self.queryset, pk=pk)
		moments = classroom.moments.all().order_by('-created')[0:20]
		serializer = MomentSerializer(moments, many=True)
		return Response(serializer.data)

	def tasks(self, request, pk):
		classroom = get_object_or_404(self.queryset, pk=pk)
		if request.method == 'GET':
			serializer = TaskSerializer(classroom.tasks.all(), many=True)
			return Response(serializer.data)
		if request.method == 'POST':
			request.data['classroom'] = classroom.pk
			if 'due' in request.data:
				request.data['due'] = datetime.datetime.fromtimestamp(request.data['due'] / 1000)

			print request.data
			serializer = TaskSerializer(data=request.data)
			serializer.is_valid(raise_exception=True)
			serializer.save()
			return Response(status=status.HTTP_201_CREATED)

	def students(self, request, pk):
		classroom = get_object_or_404(self.queryset, pk=pk)
		serializer = BasicAccountSerializer(classroom.students, many=True)
		return Response(serializer.data)

	# Tools for upload all the courses
	@staticmethod
	def upload_all_course_info(request):
		if not request.user.is_superuser:
			return Response(status=status.HTTP_403_FORBIDDEN)
		upload = request.FILES.get('file', False)
		if upload:
			upload = request.FILES['file']
			for course in upload:
				cours = json.loads(course)
				# print cours['description']
				major, created = Major.objects.get_or_create(major_short=cours['major'])
				semester, created = Semester.objects.get_or_create(name="Spring 2017")
				try:
					class_time = cours['time'].split()
					# create class time
					time = Task.objects.create(task_name=cours['name'] + ' - ' + cours['section'],
					                           location=cours['room'], type=2)
					# TODO: FIXME: timezone error, wrong time
					if len(class_time) == 4:
						time.repeat = class_time[0]
						time.start = datetime.datetime.strptime(class_time[1], '%I:%M%p') - datetime.timedelta(minutes=1)
						time.end = datetime.datetime.strptime(class_time[3], '%I:%M%p') - datetime.timedelta(minutes=1)
						time.save()
					# create classroom
					classroom, created = Classroom.objects.get_or_create(class_code=cours['number'],
					                                                     class_number=cours['name'].split()[1],
					                                                     class_name=cours['fullName'],
					                                                     description=cours['description'],
					                                                     class_section=cours['section'],
					                                                     class_credit=cours['unit'],
					                                                     class_location=cours['room'],
					                                                     class_time=time, major=major,
					                                                     semester=semester)

					if cours['instructor1'] != 'Staff':
						cours['instructor1'].replace(',', '')
						instructor1, created = Professor.objects.get_or_create(
							first_name=cours['instructor1'].split()[0],
							last_name=cours['instructor1'].split()[1],
							major=major)
						classroom.professors.add(instructor1)
					else:
						pass

					if 'instructor2' in cours and cours['instructor2'] != 'Staff' and cours['instructor2'] != '':
						cours['instructor2'].replace(',', '')
						instructor2, created = Professor.objects.get_or_create(
							first_name=cours['instructor2'].split()[0],
							last_name=cours['instructor2'].split()[1],
							major=major)
						classroom.professors.add(instructor2)
					else:
						pass

					# save classroom to get pk in db
					classroom.save()
					# create chat room
					Room.objects.create(creator=Account.objects.get(is_superuser=True),
					                    name=cours['name'] + ' - ' + cours['section'] + ' Chat Room',
					                    classroom=classroom)
				except IntegrityError:
					raise
			return Response(status=status.HTTP_201_CREATED)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
