import pandas as pd


def modify_labels(file_path, modified_file_path, yes_labels, no_labels):
    try:
        data = pd.read_csv(file_path)
        if 'label' not in data.columns:
            raise ValueError("Column 'label' not found in the file")

        data['label'] = data['label'].replace({yes_labels: 'yes', no_labels: 'no'})
        data['label'] = data['label'].replace({'yes': 1, 'no': 0})

        data.to_csv(modified_file_path, index=False)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    file_path = '../../data/csv/train.csv'

    circle_file_path = '../../data/csv/props/circle.csv'
    vertical_file_path = '../../data/csv/props/vertical_line.csv'
    horizontal_file_path = '../../data/csv/props/horizontal_line.csv'

    circle_yes_labels = [0, 6, 8, 9]
    vertical_yes_labels = [1, 4, 5, 7]
    horizontal_yes_labels = [2, 4, 5, 7]

    circle_no_labels = [1, 2, 3, 4, 5, 7]
    vertical_no_labels = [0, 2, 3, 6, 8, 9]
    horizontal_no_labels = [0, 1, 3, 6, 8, 9]

    modify_labels(file_path, circle_file_path, circle_yes_labels, circle_no_labels)
    modify_labels(file_path, vertical_file_path, vertical_yes_labels, vertical_no_labels)
    modify_labels(file_path, horizontal_file_path, horizontal_yes_labels, horizontal_no_labels)


if __name__ == '__main__':
    main()
