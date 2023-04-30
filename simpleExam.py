from tkinter import *
from tkinter import messagebox
from threading import Timer
import configparser



class simpleQuestionsExam():
	def __init__(self, fileInitPath):
		self.loadQuestions(fileInitPath)
		self.initGui()
		self.points = 0
		self.time = 0
		pass
	
	def loadQuestions(self, fileInitPath):
		#read config file
		self.questionsList = []
		config = configparser.ConfigParser()
		config.read(fileInitPath)
		
		for section in config.sections():
			print("processing: " + section)
			questionTxt=""
			answerList=[]
			points=0
			reason=""
			for (key, val) in config.items(section):
				if key == "questiontxt":
					questionTxt = val
				elif key == "points":
					points = int(val)
				elif key == "reason":
					reason = val
				elif "answer" in key:
					answerList.append((key, val))
				else:
					print("Error, unknown " + key + " key type")
			questionD={
				"questionTxt":questionTxt,
				"answerList":answerList,
				"points":points,
				"reason":reason
			}
			self.questionsList.append(questionD)
		#print(self.questionsList)
		pass
	
	def initGui(self):
		self.window = Tk()
		self.window.geometry("1200x700")#width, height
		self.window.title("Preparation Exam")
		
		startExam = LabelFrame(self.window, width=500, height=500, text="state")
		startExam.grid(column=0, row=0, columnspan=2)
		
		self.btnStartExam = Button(startExam, text="Start Exam", command=lambda: self.startExam())
		self.btnStartExam.grid(column=0, row=0)
		
		self.pointsTxt = Label(startExam, text="Points: 0")
		self.pointsTxt.grid(column=1, row=0)
		
		self.timeTxt = Label(startExam, text="Time (s): 0")
		self.timeTxt.grid(column=2, row=0)
		pass
	
	def startExam(self):
		self.points = 0
		self.time = 0
		self.pointsTxt.configure(text = "Points: " + str(self.points))
		self.timeTxt.configure(text = "Time (s): " + str(self.time))
		
		self.questionField = LabelFrame(self.window, width=500, height=500, text="Question")
		self.questionField.grid(column=0, row=1, columnspan=4)
		self.index = 0
		self.appendWidgets(self.index)
		self.startCount()
		pass
	
	def appendWidgets(self, index):
		question = self.questionsList[self.index]
		
		self.questionTxt = Label(self.questionField, text=question["questionTxt"])
		self.questionTxt.grid(column=0, row=0, columnspan=4)
		
		self.reason = question["reason"]
		
		self.questionpoints = question["points"]
		
		self.btnAnswerList = []
		rowCount = 1
		for answerKey, answerTxt in question["answerList"]:
			if "incorrect" in answerKey:
				btnAnswer = Button(self.questionField, text=answerTxt, command=lambda: self.incorrectAns())
			else:
				btnAnswer = Button(self.questionField, text=answerTxt, command=lambda: self.correctAns())
			btnAnswer.grid(column=0, row=rowCount, columnspan=4)
			self.btnAnswerList.append(btnAnswer)
			rowCount = rowCount + 1
		self.index = self.index  + 1
		pass
	
	def correctAns(self):
		self.points = self.points + self.questionpoints
		self.pointsTxt.configure(text = "Points: " + str(self.points))
		messagebox.showinfo(title="correct", message=self.reason)
		self.nextQuestion()
		pass
	
	def incorrectAns(self):
		#self.pointsTxt.configure(text = self.points)
		messagebox.showinfo(title="incorrect", message=self.reason)
		self.nextQuestion()
		pass
	
	def nextQuestion(self):
		if self.index > (len(self.questionsList) - 1):
			self.stopCount()
			messagebox.showinfo(title="fin de examen", message="se ha terminado el examen en " + str(self.time) + " s con " + str(self.points) + " puntos.")
			self.questionField.destroy()
			return
		question = self.questionsList[self.index]
		self.appendWidgets(self.index)
		self.index = self.index + 1
		pass
	
	def startCount(self):
		self.timerSec = Timer(1.0, self.incrementTime).start()
		self.stop = False
		pass
	
	def incrementTime(self):
		self.time = self.time + 1
		if self.stop:
			return
		self.timeTxt.configure(text = "Time (s): " + str(self.time))
		self.timerSec = Timer(1.0, self.incrementTime).start()
		pass
	
	def stopCount(self):
		self.stop = True
		pass
	
	def mainloop(self):
		self.window.mainloop()
	
	
	

if __name__ == "__main__":
	examObj = simpleQuestionsExam("./questions.ini")
	examObj.mainloop()
	pass