import tkinter as tk
from tkinter import messagebox

# Predefined memory block sizes
BLOCK_SIZES = [16, 32, 64, 128]
free_lists = {size: [] for size in BLOCK_SIZES}
allocated_memory = []  # List to track allocated memory blocks

# Initialize free lists with blocks
def initialize_memory():
    for size in BLOCK_SIZES:
        free_lists[size] = [f"Block-{size}-{i}" for i in range(1, 6)]  # 5 blocks of each size

# Allocate memory
def allocate_memory(size):
    for block_size in BLOCK_SIZES:
        if block_size >= size and free_lists[block_size]:
            block = free_lists[block_size].pop(0)
            allocated_memory.append((block, size))  # Add to allocated memory
            update_ui()
            return f"Allocated {block} of size {block_size} bytes"
    return "No suitable block found for allocation"

# Deallocate memory
def deallocate_memory(block):
    for i, (allocated_block, size) in enumerate(allocated_memory):
        if allocated_block == block:
            allocated_memory.pop(i)
            for block_size in BLOCK_SIZES:
                if block_size >= size:
                    free_lists[block_size].append(block)
                    update_ui()
                    return f"Deallocated {block}"
    return "Block not found in memory"

# Update the UI
def update_ui():
    for size, listbox in listboxes.items():
        listbox.delete(0, tk.END)
        for block in free_lists[size]:
            listbox.insert(tk.END, block)
    allocated_list.delete(0, tk.END)
    for block, size in allocated_memory:
        allocated_list.insert(tk.END, f"{block}: {size} bytes")

# Tkinter UI
def create_ui():
    global listboxes, allocated_list
    root = tk.Tk()
    root.title("Quick Fit Memory Management")

    tk.Label(root, text="Free Lists").grid(row=0, column=0, columnspan=4)
    
    listboxes = {}
    for i, size in enumerate(BLOCK_SIZES):
        tk.Label(root, text=f"{size} bytes").grid(row=1, column=i)
        listbox = tk.Listbox(root, width=15, height=10)
        listbox.grid(row=2, column=i)
        listboxes[size] = listbox

    tk.Label(root, text="Allocated Memory").grid(row=0, column=4)
    allocated_list = tk.Listbox(root, width=30, height=15)
    allocated_list.grid(row=1, column=4, rowspan=4)

    # Allocation Section
    tk.Label(root, text="Request Size:").grid(row=3, column=0, pady=10)
    size_entry = tk.Entry(root)
    size_entry.grid(row=3, column=1)
    tk.Button(root, text="Allocate", command=lambda: allocate(size_entry)).grid(row=3, column=2)

    # Deallocation Section
    tk.Label(root, text="Deallocate Block:").grid(row=4, column=0, pady=10)
    block_entry = tk.Entry(root)
    block_entry.grid(row=4, column=1)
    tk.Button(root, text="Deallocate", command=lambda: deallocate(block_entry)).grid(row=4, column=2)

    initialize_memory()
    update_ui()
    root.mainloop()

# Allocation Button Action
def allocate(entry):
    try:
        size = int(entry.get())
        message = allocate_memory(size)
        messagebox.showinfo("Allocation Result", message)
        entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid size")

# Deallocation Button Action
def deallocate(entry):
    block = entry.get()
    message = deallocate_memory(block)
    messagebox.showinfo("Deallocation Result", message)
    entry.delete(0, tk.END)

if __name__ == "__main__":
    create_ui()