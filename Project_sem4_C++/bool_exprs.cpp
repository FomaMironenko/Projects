#include "pch.h"

#include <iostream>
#include <fstream>
#include <cassert>
#include <string>



class BoolExpr
{
public:
	BoolExpr() = default;
	virtual ~BoolExpr() = default;

	virtual void print(std::ostream &os) const = 0;
	virtual BoolExpr *simplify() = 0;
	virtual BoolExpr *copy() const = 0;
};


class Const : public BoolExpr
{
public:
	Const(bool val): val(val)
	{	}
	~Const() = default;

	void print(std::ostream &os) const
	{
		os << std::boolalpha << val;
	}
	BoolExpr *simplify()
	{
		return new Const(val);
	}
	BoolExpr *copy() const
	{
		return new Const(val);
	}

	bool val;
};


class Var: public BoolExpr
{
public:
	Var()
	{	}
	~Var() = default;

	static void setVal(bool val)
	{
		state = val ? True : False;
	}
	static void unsetVal()
	{
		state = NotSet;
	}

	void print(std::ostream &os) const
	{
		os << std::boolalpha;
		if (state != NotSet)
		{
			os << (state == True ? true : false);
			return;
		}
		os << 'x';
	}
	BoolExpr *simplify()
	{
		if (state != NotSet)
		{
			return new Const(state == True ? true : false);
		}
		return new Var();
	}
	BoolExpr *copy() const
	{
		return new Var();
	}

	static enum state_ty { NotSet = -1, False = 0, True = 1} state;
};
Var::state_ty Var::state = Var::NotSet;


class Not : public BoolExpr
{
public:
	Not(BoolExpr* source): expr(source)
	{	}
	~Not()
	{
		delete expr;
	}

	BoolExpr *copy() const
	{
		return new Not(expr->copy());
	}
	void print(std::ostream &os) const
	{
		os << "-";
		expr->print(os);
	}
	BoolExpr *simplify(); // implemented outside

	static Not *build(const BoolExpr &other)
	{
		return new Not(other.copy());
	}

	BoolExpr *expr;
};


class And : public BoolExpr
{
public:
	And(BoolExpr *_left, BoolExpr *_right) :
		left (_left),
		right(_right)
	{	}
	~And()
	{
		delete left;
		delete right;
	}

	void print(std::ostream &os) const
	{
		os << "( ";
		left->print(os);
		os << " && ";
		right->print(os);
		os << " )";
	}
	BoolExpr *copy() const
	{
		return new And(left->copy(), right->copy());
	}
	BoolExpr *simplify(); // implemented outside

	static And *build(const BoolExpr &lhs, const BoolExpr &rhs)
	{
		return new And(lhs.copy(), rhs.copy());
	}

	BoolExpr *left, *right;
};


class Or : public BoolExpr
{
public:
	Or(BoolExpr *_left, BoolExpr *_right) :
		left (_left),
		right(_right)
	{	}
	~Or()
	{
		delete left;
		delete right;
	}

	void print(std::ostream &os) const
	{
		os << "( ";
		left->print(os);
		os << " || ";
		right->print(os);
		os << " )";
	}
	BoolExpr *copy() const
	{
		return new Or(left->copy(), right->copy());
	}
	BoolExpr *simplify(); // implemented outside

	static Or *build(const BoolExpr &lhs, const BoolExpr &rhs)
	{
		return new Or(lhs.copy(), rhs.copy());
	}

	BoolExpr *left, *right;
};


BoolExpr* Not::simplify()
{
	BoolExpr *tmp = expr->simplify();

	if (Const *ans = dynamic_cast<Const*>(tmp))
	{
		tmp = new Const(!ans->val); // tmp и ans указывают на одну и ту же память
		delete ans;
		return tmp;
	}
	if (Var   *ans = dynamic_cast<Var*>(tmp))
	{
		return new Not(tmp);
	}
	if (Not   *ans = dynamic_cast<Not*>(tmp))
	{
		tmp = ans->expr->copy();
		delete ans;
		return tmp;
	}
	if (And   *ans = dynamic_cast<And*>(tmp))
	{
		assert(false && "incomplete invariant");

		/*Or tmp (	new Not( ans->left  ), 
					new Not( ans->right ) );	// De Morgan
		delete ans;
		return tmp.simplify();*/
	}
	if (Or    *ans = dynamic_cast<Or*> (tmp))
	{
		assert(false && "incomplete invariant");

		/*And tmp (	new Not(ans->left  ),
					new Not(ans->right ) );		// De Morgan
		delete ans;
		return tmp.simplify();*/
	}
	assert(false);
}

BoolExpr* And::simplify()
{
	BoolExpr *lhs = left->simplify();
	if (Const *clhs = dynamic_cast<Const*>(lhs))
	{
		if (!clhs->val)
		{
			delete lhs;
			return new Const(false);
		}
		delete lhs;
		return right->simplify();
	}

	BoolExpr *rhs = right->simplify();
	if (Const *crhs = dynamic_cast<Const*>(rhs))
	{
		if (!crhs->val)
		{
			delete rhs;
			delete lhs;
			return new Const(false);
		}
		delete rhs;
		return lhs;
	}

	// both are not constants, so they're either Var or Not(Var)
	if (Var *vlhs = dynamic_cast<Var*>(lhs))
	{
		// lhs ~ Var   rhs ~ Not
		if (Not *nrhs = dynamic_cast<Not*>(rhs))
		{
			delete lhs;
			delete rhs;
			return new Const(false);
		}
		// both ~ Var
		delete rhs;
		return vlhs;
	}
	// lhs ~ Not   rhs ~ Var
	if (Var *vrhs = dynamic_cast<Var*>(rhs))
	{
		delete lhs;
		delete rhs;
		return new Const(false);
	}
	// both ~ Not
	delete rhs;
	return lhs;
}

BoolExpr* Or::simplify()
{
	BoolExpr *lhs = left->simplify();
	if (Const *clhs = dynamic_cast<Const*>(lhs))
	{
		if (clhs->val)
		{
			delete lhs;
			return new Const(true);
		}
		delete lhs;
		return right->simplify();
	}

	BoolExpr *rhs = right->simplify();
	if (Const *crhs = dynamic_cast<Const*>(rhs))
	{
		if (crhs->val)
		{
			delete rhs;
			delete lhs;
			return new Const(true);
		}
		delete rhs;
		return lhs;
	}

	// both are not constants, so they're either Var or Not(Var)
	if (Var *vlhs = dynamic_cast<Var*>(lhs))
	{
		// lhs ~ Var   rhs ~ Not
		if (Not *nrhs = dynamic_cast<Not*>(rhs))
		{
			delete lhs;
			delete rhs;
			return new Const(true);
		}
		// both ~ Var
		delete rhs;
		return vlhs;
	}
	// lhs ~ Not   rhs ~ Var
	if (Var *vrhs = dynamic_cast<Var*>(rhs))
	{
		delete lhs;
		delete rhs;
		return new Const(true);
	}
	// both ~ Not
	delete rhs;
	return lhs;
}




void fprint(std::ofstream os, const BoolExpr &expr)
{
	expr.print(os);
}

#define HEADER(n) "\n" + std::string(10, '-') + " test" + std::to_string(n) + " " + std::string(10, '-') + "\n\n"
#define ENDHEADER(n) "\n\n" + std::string(10, '~') + " test" + std::to_string(n) + " " + std::string(10, '~') + "\n\n"

void test1()
{
	std::cout << HEADER(1);

	Var x;
	Const a(true);
	And *b = And::build(x, a);
	BoolExpr *rez = b->simplify();

	b->print(std::cout);
	std::cout << "\n\n";
	rez->print(std::cout);

	std::cout << ENDHEADER(1) << "\n\n";
}

void test2()
{
	std::cout << HEADER(2);

	Var x;
	Not *n  = Not::build(x);
	And *a1 = And::build(x, *n);
	BoolExpr *rez = a1->simplify();

	a1->print(std::cout);
	std::cout << "\n\n";
	rez->print(std::cout);

	std::cout << ENDHEADER(2) << "\n\n";
}

void test3()
{
	std::cout << HEADER(3);

	Var x;
	Const F(false);
	Not *n = Not::build(x);
	And *a1 = And::build(x, *n);
	And *a2 = And::build(*a1, x);
	Or  *o2 = Or::build(*a2, F);
	BoolExpr *rez = o2->simplify();

	o2->print(std::cout);
	std::cout << "\n\n";
	rez->print(std::cout);

	std::cout << ENDHEADER(3) << "\n\n";
}

void test4()
{
	std::cout << HEADER(4);

	Var x;
	Not *n1 = Not::build(x);
	Not *n2 = Not::build(*n1);
	Not *n3 = Not::build(*n2);
	And *a  = And::build(*n3, *n1);
	BoolExpr *rez = a->simplify();

	a->print(std::cout);
	std::cout << "\n\n";
	rez->print(std::cout);


	std::cout << ENDHEADER(4) << "\n\n";
}


int main()
{
	test1();
	test2();
	test3();
	test4();


    return EXIT_SUCCESS; 
}