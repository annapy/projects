#High school Class

coursename = {'English':001, 'Math':002, 'Physics':003, 'Chemistry':004, 'Biology':005}

classname     = {'Junior': 9, 'Senior': 10, 'Freshman':11, 'Sophomore':12}

class Course(object):

   def __init__ (self, coursename, classname, profname, gradescheme, stu_list=None, no_enrollments=0):
       print 'in Course'
       self.coursename     = coursename
       self.classname      = classname
       self.profname       = profname
       self.grading_scheme = gradescheme
       if stu_list is None:
           self.stu_list = []
       self.no_enrollments = no_enrollments

   def tbd(no_enrollments):
       pass
      # Grades
      # Assignments

   def addstudent(self,studentname):
       self.stu_list.append(studentname)
       self.no_enrollments +=1
       return None

   def delstudent(self,studentname):
       self.stu_list.remove(studentname)
       self.no_enrollments -=1
       return None

   def __repr__(self):
       return 'Course:%s \nClass:%s \nProfessor:%s \nGrade type:%s \nStudent List:%s \nNo of students:%s\n' % (self.coursename, self.classname, self.profname, self.grading_scheme, self.stu_list, self.no_enrollments)

class OnlineCourse(object):
   def __init__ (self, univname):
       print 'in OnlineCourse'
       self.univname = univname

class SpecialCourse(Course,OnlineCourse):

    #def add_video_content(self, videolecture):
    def __init__(self, videolecture, *args, **kwargs):
        self.videolecture = videolecture
        super(SpecialCourse, self).__init__(*args, **kwargs)
    def __repr__(self):
        return 'VideoLec: %s \n Course: %s \nClass:%s \nProfessor:%s \nGrade type:%s \nStudent List:%s \nNo of students:%s \n Univ: %s\n' % (self.videolecture, self.coursename, self.classname, self.profname, self.grading_scheme, self.stu_list, self.no_enrollments, self.univname)

