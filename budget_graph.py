import matplotlib.pyplot as plt

def get_budget_data():
    """Get budget data from the user."""
    categories = []
    income = []
    expenses = []
    
    print("Enter your budget data. Type 'done' when finished.")
    
    while True:
        category = input("Enter category (or 'done' to finish): ")
        if category.lower() == 'done':
            break
        categories.append(category)
        
        income_amount = float(input(f"Enter income for {category}: "))
        income.append(income_amount)
        
        expense_amount = float(input(f"Enter expense for {category}: "))
        expenses.append(expense_amount)
    
    return categories, income, expenses

def plot_budget(categories, income, expenses):
    """Plot the budget data."""
    x = range(len(categories))
    
    fig, ax = plt.subplots()
    ax.bar(x, income, width=0.4, label='Income', align='center')
    ax.bar(x, expenses, width=0.4, label='Expenses', align='edge')
    
    ax.set_xlabel('Categories')
    ax.set_ylabel('Amount')
    ax.set_title('Personal Budget')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    
    plt.show()

def main():
    categories, income, expenses = get_budget_data()
    plot_budget(categories, income, expenses)

if __name__ == "__main__":
    main()
