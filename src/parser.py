#!/usr/bin/env python
import ply.yacc as yacc
import pydot
import sys
# Get the token map from the lexer.  This is required.
from lexer import tokens
graph = pydot.Dot(graph_type='digraph')

class Node:
	uid=0
	def __init__(self,type,children,leaf,seqNo=0,order='',isLeaf=False):
		self.type = type
		Node.uid = Node.uid + 1
		self.uid = Node.uid
		self.name = type+"##"+str(self.uid)
		if isLeaf:
			self.node = pydot.Node(self.name, style="filled", fillcolor="green", myNo = seqNo)
		else:
			self.node = pydot.Node(self.name, style="filled", fillcolor="red", myNo = seqNo)
		graph.add_node(self.node)
		self.children = children
		self.leaf = leaf
		count = 1
		leafno = 0
		childno = 0
		for letter in order:
			if letter == 'l':
				if leaf[leafno] != None:
					term = Node(leaf[leafno], [], [],seqNo = count, isLeaf=True).name
					graph.add_edge(pydot.Edge(self.name, term))
					count = count + 1
				leafno = leafno + 1
			elif letter == 'c':
				if children[childno] != None:
					graph.add_edge(pydot.Edge(self.name, children[childno]))
					# mynode = graph.get_node("EndStatement 1")
					mynodes = graph.get_nodes()
					for nodes in mynodes:
					# graph.write_png('debug.png')
						if nodes.get_name() == children[childno]:
							nodes.set("myNo", count)
					count = count + 1
				childno = childno + 1

def p_CompilationUnit(p):
	'''CompilationUnit : ImportDeclarationss ClassObjectsList'''
						# | ClassesObjects'''
	if len(p)==3:
		p[0] = Node("CompilationUnit", [p[1], p[2]],[], order="cc").name
	# else:
	# 	p[0] = Node("CompilationUnit", [p[1]],[]).name
def p_ImportDeclarationss(p):
	'''ImportDeclarationss : ImportDeclarations
							| empty'''
	if(p[1] == None):
		pass
	elif "ImportDeclarations" in p[1]:
		p[0] = Node("ImportDeclarationss",[p[1]],[], order="c")
#<import declarations> ::= <import declaration> | <import declarations> <import declaration>

def p_ImportDeclarations(p):
	'''	ImportDeclarations : ImportDeclaration 
							| ImportDeclarations ImportDeclaration'''
	if len(p)==3:
		p[0] = Node("ImportDeclarations", [p[1], p[2]],[], order="cc").name
	else:
		p[0] = Node("ImportDeclarations", [p[1]],[], order="c").name

#<import declaration> ::= import <type name> ;

def p_ImportDeclaration(p):
	'''ImportDeclaration : R_IMPORT AmbiguousName'''
	p[0] = Node("ImportDeclaration", [p[2]],[p[1]], order = "lc").name


def p_ClassObjectsList(p):
	'''ClassObjectsList : ClassObjectsList ClassAndObjectDeclaration
						| ClassAndObjectDeclaration'''
	if len(p) ==2:
		p[0] = Node('ClassObjectsList',[p[1]],[], order="c").name
	else:
		p[0] = Node('ClassObjectsList',[p[1],p[2]],[], order = "cc").name
#<classes_objects> ::= <class_object> | <class_object> <classes_objects>
def p_ClassAndObjectDeclaration(p):
	'''ClassAndObjectDeclaration : ObjectDeclaration
								| ClassDeclaration'''
	p[0] = Node('ClassAndObjectDeclaration',[p[1]],[], order="c").name


#<object_declaration> ::= object <identifier> <super>? { method_body }
def p_ObjectDeclaration(p):
	'''ObjectDeclaration :  R_OBJECT ID Super Block'''
	p[0] = Node("ObjectDeclaration", [ p[3], p[4]],[p[1],p[2]], order="llcc").name

#<class_declaration> ::= class <identifier> <class_header> <super>? { <class body declarations>? }

def p_ClassDeclaration(p):
	'''ClassDeclaration :  R_CLASS ID ClassHeader Super BLOCKOPEN ClassBodyDeclarations BLOCKCLOSE
					 | R_CLASS ID ClassHeader Super BLOCKOPEN  BLOCKCLOSE'''
	# R_CLASS Identifier ClassHeader BLOCKOPEN ClassBodyDeclarations BLOCKCLOSE
	# 				 |
	# 				 	 | R_CLASS Identifier ClassHeader BLOCKOPEN  BLOCKCLOSE
				
	if len(p)==8:
		p[0] = Node("ClassDeclaration", [p[3], p[4], p[6]],[p[1],p[2],p[5], p[7]], order="llcclcl").name
	# elif "Super" in p[4]:
	# 	p[0] = Node("ClassDeclaration", [p[2], p[3], p[4]],[p[1], p[5], p[6]]).name
	elif len(p)==7:
		p[0] = Node("ClassDeclaration", [p[3], p[4]],[p[1],p[2],p[5], p[6]], order="llccll").name
# 	else:
# 		p[0] = Node("ClassDeclaration", [p[2], p[3]],[p[1], p[4], p[5]]).name
# #<super> ::= extends <class type>

def p_Super(p):
	'''Super : R_EXTENDS ClassType
			| empty'''
	if(p[1] == None):
		pass
	elif len(p) == 3:
		p[0] = Node("Super", [p[2]],[p[1]], order="lc").name
#<class_header> ::= ( <formal parameter list>? )
def p_ClassHeader(p):
	'''ClassHeader : LPARAN FormalParameterLists RPARAN'''
	# if len(p)==3:
	# 	p[0] = Node("ClassHeader", [],[p[1], p[2]]).name
	# else:
	p[0] = Node("ClassHeader", [p[2]],[p[1], p[3]], order="lcl").name

def p_FormalParameterLists(p):
	'''FormalParameterLists : FormalParameterList
							| empty'''
	if(p[1] == None):
		pass
	elif 'FormalParameterList' in p[1]:
		p[0] = Node('FormalParameterList',[p[1]],[],order="c")

#<class body declarations> ::= <class body declaration> | <class body declarations> <class body declaration>
def p_ClassBodyDeclarations(p):
	'''ClassBodyDeclarations : ClassBodyDeclaration
							 | ClassBodyDeclarations ClassBodyDeclaration'''
	if len(p)==3:
		p[0] = Node("ClassBodyDeclarations", [p[1], p[2]],[], order="cc").name
	else:
		p[0] = Node("ClassBodyDeclarations", [p[1]],[], order="c").name
#<class body declaration> ::= <field declaration> | <method declaration>
def p_ClassBodyDeclaration(p):
	'''ClassBodyDeclaration : FieldDeclaration
							| MethodDeclaration'''
	if "FieldDeclaration" in p[1]:
		p[0] = Node("ClassBodyDeclaration", [p[1]],[], order="c").name
	else:
		p[0] = Node("ClassBodyDeclaration", [p[1]],[]).name

#<formal parameter list> ::= <formal parameter> | <formal parameter list> , <formal parameter>
def p_FormalParameterList(p):
	'''FormalParameterList : ID COLON Type 
							| ID COLON Type COMMA FormalParameterList'''
	if len(p)==4:
		p[0] = Node("FormalParameterList", [p[3]],[p[1],p[2]], order="llc").name
	else:
		p[0] = Node("FormalParameterList", [p[3], p[5]],[p[1],p[2], p[4]], order="llclc").name

#<field declaration> ::=  val <variable declarator> ;
def p_FieldDeclaration(p):
	'''FieldDeclaration : R_VAL VariableDeclarator1 EndStatement
						|  R_VAR VariableDeclarator1 EndStatement'''
	p[0] = Node("FieldDeclaration", [p[2], p[3]],[p[1]], order="lcc").name
#<variable declarator> ::= <identifier> | <identifier>: <type>   | <identifier> <variable_declarator_extra> 

def p_VariableDeclarator1(p):
	''' VariableDeclarator1 : ID COLON Type EQUALASS VariableInitializer
							| ID EQUALASS VariableInitializer'''
	if len(p)==4:
		p[0] = Node("VariableDeclarator1", [p[3]],[p[1],p[2]], order="llclc").name
	else:
		p[0] = Node("VariableDeclarator1", [p[3], p[5]],[p[1],p[2], p[4]], order="llc").name					

def p_FuncArgumentListExtras(p):
	''' FuncArgumentListExtras : VariableDeclarators
								| empty'''
	if(p[1] == None):
		pass
	else:
		p[0] = Node("FuncArgumentListExtras", [p[1]],[], order="c").name

def p_VariableDeclarators(p):
	'''VariableDeclarators : VariableDeclarator
						| VariableDeclarator COMMA VariableDeclarators'''
	if len(p)==4:
		p[0] = Node("VariableDeclarators", [p[1], p[3]],[p[2]], order="clc").name
	else:
		p[0] = Node("VariableDeclarators", [p[1]],[], order="c").name
						
def p_VariableDeclarator(p):
	'''VariableDeclarator : ID COLON Type '''
	p[0] = Node("VariableDeclarator", [p[3]],[p[1],p[2]], order="llc").name

def p_VariableInitializer(p):
	'''VariableInitializer : ArrayInitializer
							| Expression
							| ClassInstanceCreationExpression'''
	p[0] = Node("VariableInitializer", [p[1]],[], order="c").name

def p_ArrayInitializer(p):
	''' ArrayInitializer : R_NEW R_ARRAY LSQRB Type RSQRB LPARAN INT RPARAN
							| R_ARRAY LPARAN ArgumentLists RPARAN'''
	if len(p) == 9:
		p[0] = Node('ArrayInitializer',[p[4]],[p[1],p[2],p[3],p[5],p[6],p[7],p[8]], order="lllcllll").name
	else:
		p[0] = Node('ArrayInitializer',[p[3]],[p[1],p[2],p[4]], order="llcl").name

def p_EndStatement(p):
	'''EndStatement : SEMICOLON 
					| LINEFEED'''
	p[0] = Node("EndStatement", [],[p[1]], order="l").name
#<method declaration> ::= <method header> <method body>
def p_MethodDeclaration(p):
	'MethodDeclaration : MethodHeader MethodBody'
	p[0] = Node("MethodDeclaration", [p[1], p[2]],[], order="cc").name
#<method header> ::= def <method declarator> : <type> = | def <method declarator> = 
def p_MethodHeader(p):
	'''MethodHeader : R_DEF MethodDeclarator MethodReturnTypeExtras'''
	p[0] = Node("MethodHeader", [p[2], p[3]],[p[1]], order="lcc").name
#<method declarator> ::= <identifier> ( <formal parameter list>? )
def p_MethodDeclarator(p):
	'''MethodDeclarator : ID LPARAN FuncArgumentListExtras RPARAN'''
	# if len(p)==4:
	# 	p[0] = Node("MethodDeclarator", [p[1]],[p[2], p[3]]).name
	# else:
	p[0] = Node("MethodDeclarator", [p[3]],[p[1],p[2], p[4]], order="llcl").name

def p_MethodReturnTypeExtras(p):
	'''MethodReturnTypeExtras : COLON MethodReturnType EQUALASS
								| EQUALASS
								| empty '''
	if(p[1] == None):
		pass
	elif len(p)==4:
		p[0] = Node("MethodReturnTypeExtras", [p[2]],[p[1], p[3]], order="lcl").name
	elif "=" in p[1]:
		p[0] = Node("MethodReturnTypeExtras", [p[1]],[], order="c").name

def  p_MethodReturnType(p):
	'''MethodReturnType : Type 
						| R_UNIT'''
	if "Type" in p[1]:
		p[0] = Node("MethodReturnType", [p[1]],[], order="c").name
	else:
		p[0] = Node("MethodReturnType", [],[p[1]], order="l").name

#<method body> ::= <block> | ;
def p_MethodBody(p):
	'''MethodBody : Block'''
	p[0] = Node("MethodBody", [p[1]],[], order="c").name

#<type> ::= <primitive type> | <reference type>
def p_Type(p):
	'''Type : PrimitiveType 
		| ReferenceType'''
	if "PrimitiveType" in p[1]:
		p[0] = Node("Type", [p[1]],[], order="c").name
	else:
		p[0] = Node("Type", [p[1]],[], order="c").name

#<primitive type> ::= <numeric type> | boolean
def p_PrimitiveType(p):
	'''PrimitiveType : NumericType 
					| R_BOOLEAN'''
	if "NumericType" in p[1]:
		p[0] = Node("PrimitiveType", [p[1]],[], order="c").name
	else:
		p[0] = Node("PrimitiveType", [],[p[1]], order="l").name

#<numeric type> ::= <integral type> | <floating-point type>
def p_NumericType(p):
	'''NumericType : IntegralType
				| FloatingPointType'''
	if "IntegralType" in p[1]:
		p[0] = Node("NumericType", [p[1]],[], order="c").name
	else:
		p[0] = Node("NumericType", [p[1]],[], order="c").name

#<integral type> ::= byte | short | int | long | char

def p_IntegralType(p):
	'''IntegralType : R_BYTE
				 | R_SHORT
				 | R_INT
				 | R_LONG 
				 | R_CHAR'''
	p[0] = Node("IntegralType", [],[p[1]], order="l").name

#<floating-point type> ::= float | double
def p_FloatingPointType(p):
	'''FloatingPointType : R_FLOAT 
						| R_DOUBLE'''
	p[0] = Node("FloatingPointType", [],[p[1]], order="l").name

#<reference type> ::= <class type> | <array type>
def p_ReferenceType(p):
	'''ReferenceType : ID
					| ArrayType'''
	if "ArrayType" in p[1]:
		p[0] = Node("ReferenceType", [p[1]],[], order="c").name
	else:
		p[0] = Node("ReferenceType", [],[p[1]], order="l").name

#<class type> ::= <type name>
def p_ClassType(p):
	'''ClassType : ID
				 |	R_WITH ClassType'''
	if len(p) == 2:
		p[0] = Node("ClassType", [ ] ,[p[1]], order="l").name
	else:
		p[0] = Node("ClassType", [p[2]],[p[1]], order="lc").name
#<array type> ::= <type> [ ]
def p_ArrayType(p):
	'''ArrayType : R_ARRAY LSQRB RSQRB
				| R_LIST LSQRB RSQRB'''
	p[0] = Node("ArrayType", [p[1], p[2], p[3]],[], order="lll").name

#<block> ::= { <block statements>? }
def p_Block(p):
	'''Block : BLOCKOPEN BLOCKCLOSE
			| BLOCKOPEN BlockStatements BLOCKCLOSE'''
	if len(p)==3:
		p[0] = Node("Block", [],[p[1], p[2]], order="ll").name
	else:
		p[0] = Node("Block", [p[2]],[p[1], p[3]], order="lcl").name
#<block statements> ::= <block statement> | <block statements> <block statement>
def p_BlockStatements(p):
	'''BlockStatements : BlockStatement 
					| BlockStatements BlockStatement'''
	if len(p)==2:
		p[0] = Node("BlockStatements", [p[1]],[], order="c").name
	else:
		p[0] = Node("BlockStatements", [p[1],p[2]],[], order="cc").name				
#<block statement> ::= <local variable declaration statement> | <statement>
def p_BlockStatement(p):
	'''BlockStatement : LocalVariableDeclarationStatement 
					| Statement
					| MethodDeclaration'''
	if "Statement" in p[1]:
		p[0] = Node("BlockStatement", [p[1]],[], order="c").name
	else:
		p[0] = Node("BlockStatement", [p[1]],[], order="c").name
#<local variable declaration statement> ::= <local variable declaration> ;
def p_LocalVariableDeclarationStatement(p):
	'LocalVariableDeclarationStatement : LocalVariableDeclaration EndStatement'
	p[0] = Node("LocalVariableDeclarationStatement", [p[1],p[2]],[], order="cc").name	
#<local variable declaration> ::= <type> <variable declarators>
def p_LocalVariableDeclaration(p):
	'''LocalVariableDeclaration : R_VAL VariableDeclarationBody
								| R_VAR VariableDeclarationBody'''
	p[0] = Node("LocalVariableDeclaration", [p[2]],[p[1]], order="lc").name

def p_VariableDeclarationBody(p):
	'''VariableDeclarationBody : ID COLON Type EQUALASS VariableInitializer
		| ID EQUALASS VariableInitializer''' 
	if len(p) == 6:
		p[0] = Node('VariableDeclarationBody',[p[3],p[5]],[p[1],p[2],p[4]], order="llclc").name
	else:
		p[0] = Node('VariableDeclarationBody',[p[3]],[p[1],p[2]], order="llc").name
#<statement> ::= <statement without trailing substatement> | <if then statement> | <if then else statement> 
# | <while statement> | <for statement>
def p_Statement(p):
	'''Statement : StatementWithoutTrailingSubstatement
				| IfThenStatement
				| IfThenElseStatement
				| WhileStatement
				| ForStatement'''
	p[0] = Node("Statement", [p[1]],[],order='c').name

#<statement without trailing substatement> ::= <block> | <empty statement> | <expression statement> 
# | <switch statement> | <break statement> | <continue statement> | <return statement>
def p_StatementWithoutTrailingSubstatement(p):
	'''StatementWithoutTrailingSubstatement : Block
										| EmptyStatement
										| ExpressionStatement
										| SwitchStatement
										| BreakStatement
										| ContinueStatement
										| ReturnStatement'''
	p[0] = Node("StatementWithoutTrailingSubstatement", [p[1]],[],order='c').name

# <statement no short if> ::= <statement without trailing substatement> | <if then else statement no short if> 
# | <while statement no short if> | <for statement no short if>
def p_StatementNoShortIf(p):
	'''StatementNoShortIf : StatementWithoutTrailingSubstatement
						| IfThenElseStatementNoShortIf'''
	p[0] = Node("StatementNoShortIf", [p[1]],[],order='c').name

#<empty statement> ::= ;
def p_EmptyStatement(p):
	'EmptyStatement : EndStatement'
	p[0] = Node("EmptyStatement", [p[1]],[],order='c').name

#<expression statement> ::= <statement expression> ;
def p_ExpressionStatement(p):
	'ExpressionStatement : StatementExpression EndStatement'
	p[0] = Node("ExpressionStatement", [p[1],p[2]],[],order='cc').name

#<statement expression> ::= <assignment> | <preincrement expression> 
# | <postincrement expression> | <predecrement expression> | <postdecrement expression> 
# | <method invocation> | <class instance creation expression>
def p_StatementExpression(p):
	'''StatementExpression : Assignment
						| MethodInvocation
						| ClassInstanceCreationExpression'''
						# | PreincrementExpression
						# | PostincrementExpression
						# | PredecrementExpression
						# | PostdecrementExpression
	p[0] = Node("StatementExpression", [p[1]],[],order='c').name

def p_IfThenStatement(p):
	'IfThenStatement : R_IF LPARAN Expression RPARAN Statement'
	p[0] = Node("IfThenStatement", [p[3], p[5]],[p[1], p[2], p[4]],order='llclc').name

def p_IfThenElseStatement(p):
	'IfThenElseStatement : R_IF LPARAN Expression RPARAN StatementNoShortIf R_ELSE Statement'
	p[0] = Node("IfThenElseStatement", [p[3], p[5], p[7]],[p[1], p[2], p[4], p[6]],order='llclclc').name

def p_IfThenElseStatementNoShortIf(p):
	'IfThenElseStatementNoShortIf : R_IF LPARAN Expression RPARAN StatementNoShortIf R_ELSE StatementNoShortIf'
	p[0] = Node("IfThenElseStatementNoShortIf", [p[3], p[5], p[7]],[p[1], p[2], p[4], p[6]],order='llclclc').name

def p_SwitchStatement(p):
	'SwitchStatement :  Expression  R_MATCH SwitchBlock'
	p[0] = Node("SwitchStatement", [p[1], p[3]],[p[2]],order='clc').name


def p_SwitchBlock(p):
	'''SwitchBlock : BLOCKOPEN SwitchBlockStatementGroups SwitchLabels BLOCKCLOSE
				| BLOCKOPEN  SwitchLabels BLOCKCLOSE
				| BLOCKOPEN SwitchBlockStatementGroups  BLOCKCLOSE
				| BLOCKOPEN   BLOCKCLOSE'''
	if len(p) ==  5:
		p[0] = Node("SwitchBlock", [p[2], p[3]],[p[1],p[4]],order='lccl').name
	elif "SwitchLabels" in p[2]:
		p[0] = Node("SwitchBlock", [p[2]],[p[1],p[3]],order='lcl').name
	elif "SwitchBlockStatementGroups" in p[2]:
		p[0] = Node("SwitchBlock", [p[2]],[p[1],p[3]],order='lcl').name
	else:
		p[0] = Node("SwitchBlock", [], [p[1], p[2]],order='ll')

def p_SwitchBlockStatementGroups(p):
	'''SwitchBlockStatementGroups : SwitchBlockStatementGroup
									 | SwitchBlockStatementGroups SwitchBlockStatementGroup'''
	if len(p) ==  3:
		p[0] = Node("SwitchBlockStatementGroups", [p[1], p[2]],[],order='c').name
	else:
		p[0] = Node("SwitchBlockStatementGroups", [p[1]],[],order='cc').name

def p_SwitchBlockStatementGroup(p):
	'SwitchBlockStatementGroup : SwitchLabels BlockStatements'
	p[0] = Node("SwitchBlockStatementGroup", [p[1], p[2]],[],order='cc').name

def p_SwitchLabels(p):
	'''SwitchLabels : SwitchLabel 
					| SwitchLabels SwitchLabel'''
	if len(p) ==  3:
		p[0] = Node("SwitchLabels", [p[1], p[2]],[],order='cc').name
	else:
		p[0] = Node("SwitchLabels", [p[1]],[],order='c').name

def p_SwitchLabel(p):
	'''SwitchLabel : R_CASE Expression COLON 
				| R_DEFAULT COLON'''
	if len(p) ==  3:
		p[0] = Node("SwitchLabel", [p[2]],[p[1], p[3]],order='lcl').name
	else:
		p[0] = Node("SwitchLabel", [],[p[1], p[2]],order='ll').name

def p_WhileStatement(p):
	'WhileStatement :  R_WHILE  LPARAN Expression RPARAN Statement'
	p[0] = Node("WhileStatement", [p[3], p[5]],[p[1], p[2], p[4]],order='llclc').name

def p_ForStatement(p): 
	'ForStatement : R_FOR LPARAN ForExprs RPARAN Statement'
	p[0] = Node("ForStatement", [p[3], p[5]],[p[1], p[2], p[4]],order='llclc').name


def p_ForExprs(p):
	'''ForExprs :  ForVariables EndStatement ForExprs 
			| ForVariables'''
	if len(p) ==  4:
		p[0] = Node("ForExprs", [p[1],p[2],p[3]], [],order='ccc').name
	else:
		p[0] = Node("ForExprs", [p[1]],[],order='c').name

#''' for_variables : declaration_keyword_extras IDENTIFIER IN expression for_untilTo expression '''
def p_ForVariables(p): 
	'ForVariables : DeclarationKeywordExtras ID R_LEFTARROW1 Expression ForUntilTo Expression' 
	p[0] = Node("ForVariables", [p[1],p[4],p[5],p[6]], [p[2],p[3]],order='cllccc').name
 #'''declaration_keyword_extras : variable_header | empty'''	
#'''variable_header : K_VAL | K_VAR '''
def p_DeclarationKeywordExtras(p):
	'''DeclarationKeywordExtras : VariableHeader 
								| empty'''
	if(p[1] == None):
		pass
	elif 'VariableHeader' in p[1]:
		p[0] = Node('DeclarationKeywordExtras',[p[1]],[],order='c').name

def p_VariableHeader(p):
	'''VariableHeader : R_VAL
					| R_VAR'''
	p[0] = Node('VariableHeader',[],[p[1]],order='l').name

def p_ForUntilTo(p):
	'''ForUntilTo : R_UNTIL 
				| R_TO'''
	p[0] = Node("ForUntilTo", [],[p[1]],order='l').name


def p_BreakStatement(p) :
	'''BreakStatement : R_BREAK ID EndStatement
					| R_BREAK EndStatement'''
	if len(p) ==  4:
		p[0] = Node("BreakStatement", [p[3]], [p[1]],[p[2]],order='llc').name
	else:
		p[0] = Node("BreakStatement", [p[2]],[p[1]],order='lc').name

def p_ContinueStatement(p):
	'''ContinueStatement : R_CONTINUE ID EndStatement
						| R_CONTINUE  EndStatement'''
	if len(p) ==  4:
		p[0] = Node("ContinueStatement", [p[3]], [p[1]],[p[2]],order='llc').name
	else:
		p[0] = Node("ContinueStatement", [p[2]],[p[1]],order='lc').name

def p_ReturnStatement(p):
	'''ReturnStatement : R_RETURN Expression EndStatement
					| R_RETURN EndStatement'''
	if len(p) ==  4:
		p[0] = Node("ReturnStatement", [p[2],p[3]], [p[1]],order='lcc').name
	else:
		p[0] = Node("ReturnStatement", [p[2]],[p[1]],order='lc').name


def p_Expression(p):
	'''Expression : Assignment
					| OrExpression'''
	p[0] = Node("Expression", [p[1]],[],order='c').name


# def p_CondititionalExpression(p): 
# 	'''  CondititionalExpression : OrExpression
# 			|  OrExpression Expression COLON CondititionalExpression
# 									| Expression COLON CondititionalExpression'''


def p_LeftHandSide(p):
	'''LeftHandSide : AmbiguousName
				| ArrayAccess'''
					# | FieldAccess
	p[0] = Node("LeftHandSide", [p[1]],[],order='c').name

def p_AssignmentOperator(p):
	'''AssignmentOperator : EQUALASS 
						| MULASS
						| DIVASS
						| MODASS 
						| ADDASS
						| SUBASS
						| BITLEFTASS
						| BITRIGHTASS
						| BITRSFILLASS 
						| BITANDASS 
						| BITXORASS 
						| BITORASS'''
	p[0] = Node("AssignmentOperator", [],[p[1]],order='l').name

##check it very important issue
def p_Assignment(p):
	'Assignment : LeftHandSide AssignmentOperator OrExpression'
	p[0] = Node("Assignment", [p[1], p[2], p[3]],[]).name

def p_OrExpression(p):
	'''OrExpression : AndExpression
				  | AndExpression OR OrExpression'''
	if(len(p)==2):
		p[0] = Node("OrExpression", [p[1]],[],order='c').name
	else:
		p[0] = Node("OrExpression", [p[1], p[3]],[p[2]],order='clc').name

def p_AndExpression(p):
	'''AndExpression : XorExpression 
					| AndExpression BITAND XorExpression'''
	if len(p) ==  4:
		p[0] = Node("AndExpression", [p[1],p[3]], [p[2]],order='clc').name
	else:
		p[0] = Node("AndExpression", [p[1]],[],order='c').name			

def p_XorExpression(p):
	'''XorExpression : EqualityExpression
					| XorExpression BITXOR EqualityExpression'''
	if len(p) == 2:
		p[0] = Node('XorExpression',[p[1]],[],order='c').name
	else :
		p[0] = Node('XorExpression',[p[1],p[3]],[p[2]],order='clc').name



def p_EqualityExpression(p):
	'''EqualityExpression : RelationalExpression
						 | EqualityExpression EQUAL RelationalExpression
						| EqualityExpression NOTEQUAL RelationalExpression'''
	if len(p) ==  4:
		p[0] = Node("EqualityExpression", [p[1], p[3]], [p[2]],order='clc').name
	else:
		p[0] = Node("EqualityExpression", [p[1]],[],order='c').name

def p_RelationalExpression(p):
	'''RelationalExpression : ShiftExpression 
						| RelationalExpression LT ShiftExpression 
						| RelationalExpression GT ShiftExpression  
						| RelationalExpression LE ShiftExpression  
						| RelationalExpression GE ShiftExpression  
						| RelationalExpression R_INSTANCEOF ReferenceType'''
	if len(p) ==  4:
		p[0] = Node("RelationalExpression", [p[1],p[3]], [p[2]],order='clc').name
	else:
		p[0] = Node("RelationalExpression", [p[1]],[],order='c').name

def p_ShiftExpression(p):
	'''ShiftExpression : AdditiveExpression 
					| ShiftExpression BITLSHIFT AdditiveExpression 
					| ShiftExpression BITRSHIFT AdditiveExpression 
					| ShiftExpression BITRSFILL AdditiveExpression'''
	if len(p) ==  4:
		p[0] = Node("ShiftExpression", [p[1], p[3]], [p[2]],order='clc').name
	else:
		p[0] = Node("ShiftExpression", [p[1]],[],order='c').name

# <additive expression> ::= <multiplicative expression> | <additive expression> + <multiplicative expression> | <additive expression> - <multiplicative expression>
def p_AdditiveExpression(p):
	'''AdditiveExpression : MultiplicativeExpression
							| AdditiveExpression PLUS MultiplicativeExpression
							| AdditiveExpression MINUS MultiplicativeExpression'''
	if len(p) ==  4:
		p[0] = Node("AdditiveExpression", [p[1],p[3]], [p[2]],order='clc').name
	else:
		p[0] = Node("AdditiveExpression", [p[1]],[],order='c').name

# <multiplicative expression> ::= <unary expression> | <multiplicative expression> * <unary expression> | <multiplicative expression> / <unary expression> | <multiplicative expression> % <unary expression>
def p_MultiplicativeExpression(p):
	'''MultiplicativeExpression : UnaryExpression
								| MultiplicativeExpression MULTIPLICATION UnaryExpression
								| MultiplicativeExpression DIVISION UnaryExpression
								| MultiplicativeExpression MODULUS UnaryExpression'''
	if len(p) ==  4:
		p[0] = Node("MultiplicativeExpression", [p[1], p[3]], [p[2]],order='clc').name
	else:
		p[0] = Node("MultiplicativeExpression", [p[1]],[],order='c').name

def p_UnaryExpression(p):
	'''UnaryExpression :  PLUS UnaryExpression
						| MINUS UnaryExpression
						| UnaryExpressionNotPlusMinus'''
						# | PreincrementExpression
						# | PredecrementExpression'''
	if len(p) ==  3:
		p[0] = Node("MultiplicativeExpression", [p[2]], [p[1]],order='lc').name
	else:
		p[0] = Node("MultiplicativeExpression", [p[1]],[],order='c').name

def p_UnaryExpressionNotPlusMinus(p):
	'''UnaryExpressionNotPlusMinus : PostfixExpression
									| NOT UnaryExpression'''
									#| CastExpression'''
									#| BITNEG UnaryExpression
	if len(p) ==  3:
		p[0] = Node("UnaryExpressionNotPlusMinus", [p[2]], [p[1]],order='lc').name
	else:
		p[0] = Node("UnaryExpressionNotPlusMinus", [p[1]],[],order='c').name

def p_PostfixExpression(p):
	'''PostfixExpression : Primary
							| AmbiguousName'''
							# | PostincrementExpression
							# | PostdecrementExpression'''
	p[0] = Node("PostfixExpression", [p[1]],[],order='c').name
# <method invocation> ::= <method name> ( <argument list>? ) | <primary> . <identifier> ( <argument list>? ) | super . <identifier> ( <argument list>? )
#'''method_invocation : ambiguous_name LPAREN argument_list_extras RPAREN '''
def p_MethodInvocation(p):
	'''MethodInvocation : AmbiguousName LPARAN ArgumentLists RPARAN'''
					#		| AmbiguousName LPARAN RPARAN'''
						# | Primary DOT Identifier LPARAN ArgumentList RPARAN
						# | Super DOT Identifier LPARAN ArgumentList RPARAN'''
						# # | Super DOT Identifier LPARAN RPARAN
						# | AmbiguousName LPARAN RPARAN
						# | Primary DOT Identifier LPARAN RPARAN
	if len(p) ==  5:
		p[0] = Node("MethodInvocation", [p[1], p[3]], [p[2], p[4]],order='clcl').name
	# elif len(p) ==  4:
	# 	p[0] = Node("MethodInvocation", [p[1]], [p[2], p[3]]).name

def p_ArgumentLists(p):
	'''ArgumentLists : ArgumentList
						| empty'''
	if(p[1] == None):
		pass
	elif 'ArgumentList' in p[1]:
		p[0] = Node('ArgumentLists',[p[1]],[],order='c').name

def p_Primary(p):
	'''Primary : PrimaryNoNewArray'''
				# | ArrayCreationExpression'''
	p[0] = Node('Primary',[p[1]],[],order='c').name

# <primary no new array> ::= <literal> | this | ( <expression> ) | <class instance creation expression> 
# | <field access> | <method invocation> | <array access>

def p_PrimaryNoNewArray(p):
	'''PrimaryNoNewArray : Literal
						| LPARAN Expression RPARAN
						| MethodInvocation
						| ArrayAccess'''
						# | ClassInstanceCreationExpression
						# | FieldAccess
	if len(p) == 3:
		p[0] = Node('PrimaryNoNewArray',[p[2]],[p[1],p[3]],order='lcl').name
	else:
		p[0] = Node('PrimaryNoNewArray',[p[1]],[],order='c').name
# <class instance creation expression> ::= new <class type> ( <argument list>? )

def p_ClassInstanceCreationExpression(p):
	'''ClassInstanceCreationExpression : R_NEW ID LPARAN ArgumentLists RPARAN'''
								#		| R_NEW ClassType LPARAN RPARAN'''
	if len(p) ==6:
		p[0] = Node('ClassInstanceCreationExpression',[p[4]],[p[1],p[2],p[3],p[5]],order='lllcl').name
	# else:
	# 	p[0] = Node('ClassInstanceCreationExpression',[p[2]],[p[1],p[3],p[4]]).name

# <argument list> ::= <expression> | <argument list> , <expression>
def p_ArgumentList(p):
	'''ArgumentList : Expression
					| ArgumentList COMMA Expression'''
	if len(p) == 2:
		p[0] = Node('ArgumentList',[p[1]],[],order='c').name
	else :
		p[0] = Node('ArgumentList',[p[1],p[3]],[p[2]],order='clc').name

# <array access> ::= <expression name> [ <expression> ] | <primary no new array> [ <expression>]
def p_ArrayAccess(p):
	'''ArrayAccess : AmbiguousName LSQRB Expression RSQRB'''
					# | PrimaryNoNewArray LSQRB Expression RSQRB'''
	p[0] = Node('ArrayAccess',[p[1],p[3]],[p[2],p[4]]).name

def p_AmbiguousName(p):
	'''AmbiguousName : ID 
					| AmbiguousName DOT ID'''
	if len(p)==2:
		p[0] = Node('AmbiguousName',[],[p[1]],order='l').name
	else:
		p[0] = Node('AmbiguousName',[p[1]],[p[2],p[3]],order='cll').name

# <literal> ::= <integer literal> | <floating-point literal> | <boolean literal> | <character literal> | <string literal> | <null literal>
def p_Literal(p):
	'''Literal : IntegerLiteral
				| FloatingPointLiteral
				| BooleanLiteral
				| CharacterLiteral
				| StringLiteral
				| NullLiteral'''

	p[0] = Node("Literal", [p[1]],[],order='c').name
# <integer literal> ::= <decimal integer literal> | <hex integer literal> | <octal integer literal>

def p_BooleanLiteral(p):
	'BooleanLiteral : BOOL'
	p[0] = Node('BooleanLiteral',[],[p[1]],order='l').name

def p_IntegerLiteral(p):
	 'IntegerLiteral : INT'
	 p[0] = Node('IntegerLiteral',[],[p[1]],order='l').name

def p_FloatingPointLiteral(p):
	'FloatingPointLiteral : FLOAT'
	p[0] = Node('FloatingPointLiteral',[],[p[1]],order='l').name

def p_CharacterLiteral(p):
	'CharacterLiteral : CHAR'
	p[0] = Node('CharacterLiteral',[],[p[1]],order='l').name

def p_StringLiteral(p):
	'StringLiteral : STRING'
	p[0] = Node('StringLiteral',[],[p[1]],order='l').name


# # # <null literal> ::= null
def p_NullLiteral(p):
	'NullLiteral : R_NULL'
	p[0] = Node("NullLiteral", [],[p[1]],order='l').name


def p_empty(p):
    'empty :'
    pass
parser = yacc.yacc()




if __name__ == "__main__" :
 #   filename = sys.argv[1]
    filename = "../tests/Demo.scala"
    programfile = open(filename)
    data = programfile.read()
    parser.parse(data)
    graph.write_png('parsetree.png')
    graph.to_string()
    print(graph.to_string())
