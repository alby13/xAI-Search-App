import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
import requests
import json
import threading
from datetime import datetime

# --- Configuration ---
XAI_API_URL = "https://api.x.ai/v1/chat/completions"
DEFAULT_MODEL = "grok-3-latest"

class XaiSearchApp:
    def __init__(self, root):
        self.root = root
        root.title("xAI Live Search GUI")
        root.geometry("900x750") # Increased height for more source options

        # API Key
        self.api_key_var = tk.StringVar(value=os.getenv("XAI_API_KEY", ""))

        # --- Main Paned Window for Layout ---
        main_pane = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Left Pane: Controls ---
        controls_frame = ttk.Frame(main_pane, padding="10")
        main_pane.add(controls_frame, weight=1)

        # --- Right Pane: Response ---
        response_frame = ttk.LabelFrame(main_pane, text="API Response", padding="10")
        main_pane.add(response_frame, weight=2)

        # --- Controls Widgets (Left Pane) ---
        row_idx = 0

        # API Key
        ttk.Label(controls_frame, text="xAI API Key:").grid(row=row_idx, column=0, sticky="w", pady=2)
        self.api_key_entry = ttk.Entry(controls_frame, textvariable=self.api_key_var, width=40, show="*")
        self.api_key_entry.grid(row=row_idx, column=1, columnspan=2, sticky="ew", pady=2)
        row_idx += 1

        # Prompt
        ttk.Label(controls_frame, text="Prompt:").grid(row=row_idx, column=0, sticky="nw", pady=2)
        self.prompt_text = scrolledtext.ScrolledText(controls_frame, height=5, width=40, wrap=tk.WORD)
        self.prompt_text.grid(row=row_idx, column=1, columnspan=2, sticky="ew", pady=2)
        self.prompt_text.insert(tk.END, "Provide me a digest of world news in the last 24 hours.")
        row_idx += 1

        # Model
        ttk.Label(controls_frame, text="Model:").grid(row=row_idx, column=0, sticky="w", pady=2)
        self.model_var = tk.StringVar(value=DEFAULT_MODEL)
        self.model_entry = ttk.Entry(controls_frame, textvariable=self.model_var, width=40)
        self.model_entry.grid(row=row_idx, column=1, columnspan=2, sticky="ew", pady=2)
        row_idx += 1

        # Search Parameters Frame
        search_params_frame = ttk.LabelFrame(controls_frame, text="Search Parameters", padding="10")
        search_params_frame.grid(row=row_idx, column=0, columnspan=3, sticky="ew", pady=5)
        row_idx += 1
        
        sp_row_idx = 0

        # Mode
        ttk.Label(search_params_frame, text="Mode:").grid(row=sp_row_idx, column=0, sticky="w", pady=2)
        self.mode_var = tk.StringVar(value="auto")
        self.mode_combo = ttk.Combobox(search_params_frame, textvariable=self.mode_var, values=["auto", "on", "off"], state="readonly")
        self.mode_combo.grid(row=sp_row_idx, column=1, sticky="ew", pady=2)
        sp_row_idx += 1

        # Return Citations
        self.return_citations_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(search_params_frame, text="Return Citations", variable=self.return_citations_var).grid(row=sp_row_idx, column=0, columnspan=2, sticky="w", pady=2)
        sp_row_idx += 1

        # Date Range
        ttk.Label(search_params_frame, text="From Date (YYYY-MM-DD):").grid(row=sp_row_idx, column=0, sticky="w", pady=2)
        self.from_date_var = tk.StringVar()
        ttk.Entry(search_params_frame, textvariable=self.from_date_var).grid(row=sp_row_idx, column=1, sticky="ew", pady=2)
        sp_row_idx += 1

        ttk.Label(search_params_frame, text="To Date (YYYY-MM-DD):").grid(row=sp_row_idx, column=0, sticky="w", pady=2)
        self.to_date_var = tk.StringVar()
        ttk.Entry(search_params_frame, textvariable=self.to_date_var).grid(row=sp_row_idx, column=1, sticky="ew", pady=2)
        sp_row_idx += 1

        # Max Search Results
        ttk.Label(search_params_frame, text="Max Search Results:").grid(row=sp_row_idx, column=0, sticky="w", pady=2)
        self.max_results_var = tk.StringVar(value="20")
        ttk.Entry(search_params_frame, textvariable=self.max_results_var).grid(row=sp_row_idx, column=1, sticky="ew", pady=2)
        sp_row_idx += 1

        # Sources Configuration Frame
        sources_config_frame = ttk.LabelFrame(controls_frame, text="Data Sources", padding="10")
        sources_config_frame.grid(row=row_idx, column=0, columnspan=3, sticky="ew", pady=5)
        row_idx += 1

        sc_row_idx = 0

        # --- Web Source ---
        self.use_web_var = tk.BooleanVar(value=True) # Default to web and x if no sources specified
        ttk.Checkbutton(sources_config_frame, text="Use Web Source", variable=self.use_web_var).grid(row=sc_row_idx, column=0, sticky="w")
        sc_row_idx +=1
        ttk.Label(sources_config_frame, text="  Country (Web):").grid(row=sc_row_idx, column=0, sticky="e", pady=1)
        self.web_country_var = tk.StringVar()
        ttk.Entry(sources_config_frame, textvariable=self.web_country_var, width=15).grid(row=sc_row_idx, column=1, sticky="w", pady=1)
        sc_row_idx +=1
        ttk.Label(sources_config_frame, text="  Excluded (Web, comma-sep):").grid(row=sc_row_idx, column=0, sticky="e", pady=1)
        self.web_excluded_var = tk.StringVar()
        ttk.Entry(sources_config_frame, textvariable=self.web_excluded_var, width=15).grid(row=sc_row_idx, column=1, sticky="w", pady=1)
        sc_row_idx +=1
        self.web_safe_search_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(sources_config_frame, text="  Safe Search (Web)", variable=self.web_safe_search_var).grid(row=sc_row_idx, column=0, columnspan=2, sticky="w", pady=1)
        sc_row_idx +=1
        ttk.Separator(sources_config_frame, orient='horizontal').grid(row=sc_row_idx, columnspan=2, sticky='ew', pady=5)
        sc_row_idx +=1

        # --- X Source ---
        self.use_x_var = tk.BooleanVar(value=True) # Default to web and x if no sources specified
        ttk.Checkbutton(sources_config_frame, text="Use X Source", variable=self.use_x_var).grid(row=sc_row_idx, column=0, sticky="w")
        sc_row_idx +=1
        ttk.Label(sources_config_frame, text="  X Handles (comma-sep):").grid(row=sc_row_idx, column=0, sticky="e", pady=1)
        self.x_handles_var = tk.StringVar()
        ttk.Entry(sources_config_frame, textvariable=self.x_handles_var, width=15).grid(row=sc_row_idx, column=1, sticky="w", pady=1)
        sc_row_idx +=1
        ttk.Separator(sources_config_frame, orient='horizontal').grid(row=sc_row_idx, columnspan=2, sticky='ew', pady=5)
        sc_row_idx +=1
        
        # --- News Source ---
        self.use_news_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(sources_config_frame, text="Use News Source", variable=self.use_news_var).grid(row=sc_row_idx, column=0, sticky="w")
        sc_row_idx +=1
        ttk.Label(sources_config_frame, text="  Country (News):").grid(row=sc_row_idx, column=0, sticky="e", pady=1)
        self.news_country_var = tk.StringVar()
        ttk.Entry(sources_config_frame, textvariable=self.news_country_var, width=15).grid(row=sc_row_idx, column=1, sticky="w", pady=1)
        sc_row_idx +=1
        ttk.Label(sources_config_frame, text="  Excluded (News, comma-sep):").grid(row=sc_row_idx, column=0, sticky="e", pady=1)
        self.news_excluded_var = tk.StringVar()
        ttk.Entry(sources_config_frame, textvariable=self.news_excluded_var, width=15).grid(row=sc_row_idx, column=1, sticky="w", pady=1)
        sc_row_idx +=1
        self.news_safe_search_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(sources_config_frame, text="  Safe Search (News)", variable=self.news_safe_search_var).grid(row=sc_row_idx, column=0, columnspan=2, sticky="w", pady=1)
        sc_row_idx +=1
        ttk.Separator(sources_config_frame, orient='horizontal').grid(row=sc_row_idx, columnspan=2, sticky='ew', pady=5)
        sc_row_idx +=1

        # --- RSS Source ---
        self.use_rss_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(sources_config_frame, text="Use RSS Source", variable=self.use_rss_var).grid(row=sc_row_idx, column=0, sticky="w")
        sc_row_idx +=1
        ttk.Label(sources_config_frame, text="  RSS Link (one for now):").grid(row=sc_row_idx, column=0, sticky="e", pady=1)
        self.rss_links_var = tk.StringVar()
        ttk.Entry(sources_config_frame, textvariable=self.rss_links_var, width=15).grid(row=sc_row_idx, column=1, sticky="w", pady=1)
        sc_row_idx +=1

        # Send Button
        self.send_button = ttk.Button(controls_frame, text="Send Request", command=self.start_send_request_thread)
        self.send_button.grid(row=row_idx, column=0, columnspan=3, pady=10)
        row_idx += 1
        
        # Status Label
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(controls_frame, textvariable=self.status_var).grid(row=row_idx, column=0, columnspan=3, sticky="ew", pady=2)


        # --- Response Widgets (Right Pane) ---
        self.response_text = scrolledtext.ScrolledText(response_frame, height=30, width=60, wrap=tk.WORD, state=tk.DISABLED)
        self.response_text.pack(fill=tk.BOTH, expand=True)


    def _validate_date(self, date_str):
        if not date_str:
            return True # Empty is fine
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def start_send_request_thread(self):
        # Disable button and update status
        self.send_button.config(state=tk.DISABLED)
        self.status_var.set("Sending request...")
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete(1.0, tk.END)
        self.response_text.config(state=tk.DISABLED)

        # Run the API call in a new thread
        thread = threading.Thread(target=self.send_request)
        thread.daemon = True # Allows main program to exit even if threads are running
        thread.start()

    def update_gui_after_request(self, response_data=None, error_message=None):
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete(1.0, tk.END)
        if error_message:
            self.response_text.insert(tk.END, f"Error:\n{error_message}")
            self.status_var.set("Error!")
        elif response_data:
            self.response_text.insert(tk.END, json.dumps(response_data, indent=2))
            
            # Try to extract and display citations clearly
            citations = []
            if response_data.get("choices") and response_data["choices"][0].get("message"):
                message_content = response_data["choices"][0]["message"].get("content", "")
                # The documentation says citations are in the last chunk for streaming.
                # For non-streaming, they might be elsewhere or part of the tool_calls.
                # The example shows "citations" at the top level of the response for non-streaming in their docs,
                # but it's safer to check the last chunk if it were streaming.
                # Let's assume for non-streaming, if present, it's at the choice or message level.
                # The example has citations directly in the payload of the final chunk of a stream.
                # Let's check if they appear in the response directly.
                if "citations" in response_data: # Check top level first based on their example structure for a full response
                    citations.extend(response_data["citations"])
                elif response_data["choices"][0].get("citations"):
                     citations.extend(response_data["choices"][0]["citations"])


            if citations:
                self.response_text.insert(tk.END, "\n\n--- Citations ---\n")
                for i, citation in enumerate(citations):
                    self.response_text.insert(tk.END, f"{i+1}. {citation}\n")
            self.status_var.set("Response received.")
        
        self.response_text.config(state=tk.DISABLED)
        self.send_button.config(state=tk.NORMAL)


    def send_request(self):
        api_key = self.api_key_var.get()
        prompt = self.prompt_text.get(1.0, tk.END).strip()
        model = self.model_var.get().strip()

        if not api_key:
            self.root.after(0, self.update_gui_after_request, None, "API Key is required.")
            return
        if not prompt:
            self.root.after(0, self.update_gui_after_request, None, "Prompt is required.")
            return
        if not model:
            self.root.after(0, self.update_gui_after_request, None, "Model is required.")
            return

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": model
        }

        # Build search_parameters
        search_params = {}
        search_params["mode"] = self.mode_var.get()
        if self.return_citations_var.get():
            search_params["return_citations"] = True

        from_date = self.from_date_var.get().strip()
        to_date = self.to_date_var.get().strip()
        if from_date:
            if not self._validate_date(from_date):
                self.root.after(0, self.update_gui_after_request, None, "Invalid From Date format. Use YYYY-MM-DD.")
                return
            search_params["from_date"] = from_date
        if to_date:
            if not self._validate_date(to_date):
                self.root.after(0, self.update_gui_after_request, None, "Invalid To Date format. Use YYYY-MM-DD.")
                return
            search_params["to_date"] = to_date
        
        max_results_str = self.max_results_var.get().strip()
        if max_results_str:
            try:
                search_params["max_search_results"] = int(max_results_str)
            except ValueError:
                self.root.after(0, self.update_gui_after_request, None, "Max Search Results must be an integer.")
                return
        
        # Build sources
        sources_list = []
        if self.use_web_var.get():
            web_config = {"type": "web"}
            if self.web_country_var.get(): web_config["country"] = self.web_country_var.get().strip().upper()
            if self.web_excluded_var.get(): web_config["excluded_websites"] = [site.strip() for site in self.web_excluded_var.get().split(',')]
            web_config["safe_search"] = self.web_safe_search_var.get()
            sources_list.append(web_config)

        if self.use_x_var.get():
            x_config = {"type": "x"}
            if self.x_handles_var.get(): x_config["x_handles"] = [handle.strip() for handle in self.x_handles_var.get().split(',')]
            sources_list.append(x_config)
        
        if self.use_news_var.get():
            news_config = {"type": "news"}
            if self.news_country_var.get(): news_config["country"] = self.news_country_var.get().strip().upper()
            if self.news_excluded_var.get(): news_config["excluded_websites"] = [site.strip() for site in self.news_excluded_var.get().split(',')]
            news_config["safe_search"] = self.news_safe_search_var.get()
            sources_list.append(news_config)

        if self.use_rss_var.get():
            rss_config = {"type": "rss"}
            if self.rss_links_var.get(): rss_config["links"] = [link.strip() for link in self.rss_links_var.get().split(',')] # API says one link, but docs show "links" suggesting a list
            sources_list.append(rss_config)

        if sources_list: # Only add sources if any are configured
             search_params["sources"] = sources_list
        elif not sources_list and (search_params["mode"] == "on" or search_params["mode"] == "auto"):
            # If mode is on/auto and NO sources are explicitly defined by user,
            # API defaults to web and x. We don't need to send empty "sources": []
            pass


        # Only add search_parameters to payload if it's not empty or mode is not 'off'
        if search_params["mode"] != "off" or len(search_params) > 1 : # if mode is 'off', only mode itself is needed
             payload["search_parameters"] = search_params
        elif search_params["mode"] == "off":
            payload["search_parameters"] = {"mode": "off"}


        try:
            # For debugging the payload being sent
            print("--- Payload ---")
            print(json.dumps(payload, indent=2))
            print("---------------")

            response = requests.post(XAI_API_URL, headers=headers, json=payload, timeout=30) # 30s timeout
            response.raise_for_status() # Raise an exception for HTTP errors
            response_data = response.json()
            self.root.after(0, self.update_gui_after_request, response_data, None)

        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP Error: {e.response.status_code}\n{e.response.text}"
            self.root.after(0, self.update_gui_after_request, None, error_msg)
        except requests.exceptions.RequestException as e:
            self.root.after(0, self.update_gui_after_request, None, f"Request failed: {e}")
        except Exception as e:
            self.root.after(0, self.update_gui_after_request, None, f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = XaiSearchApp(root)
    root.mainloop()
